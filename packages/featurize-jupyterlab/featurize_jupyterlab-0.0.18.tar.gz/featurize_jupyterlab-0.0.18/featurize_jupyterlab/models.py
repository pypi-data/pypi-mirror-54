import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
import enum

import stream
from sqlalchemy import (JSON, Column, DateTime, ForeignKey, Index, String,
                        Table, text, Enum)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .config import Config
from .package_manager import PackageManager
from .proto import minetorch_pb2
from .utils import dict_merge, make_tarfile, update_json_file


def _declarative_constructor(self, _session=None, **kwargs):
    self._session = _session
    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            raise TypeError(
                "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
            )
        setattr(self, k, kwargs[k])


BaseORM = declarative_base(constructor=_declarative_constructor)


class BaseModel():
    id = Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def todict(self):
        result = {}
        for column in self.__table__.columns:
            result[column.name] = str(getattr(self, column.name))
        return result


class Experiment(BaseModel, BaseORM):
    __tablename__ = 'experiments'

    name = Column(String)
    enabled_packages = Column(JSON)
    executions = relationship('Execution', backref='experiment')

    def todict(self):
        one_dict = {}
        one_dict['id'] = str(self.id)
        one_dict['created_at'] = self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        one_dict['updated_at'] = self.updated_at.strftime("%d/%m/%Y %H:%M:%S")
        one_dict['name'] = self.name
        one_dict['enabled_packages'] = self.enabled_packages
        return one_dict

    def prepare_directories(self):
        try:
            os.makedirs(self.dir())
        except FileExistsError:
            pass

    def dir(self):
        return Path() / '.featurize_experiments' / str(self.id)

    def update_config(self, config):
        one_versoin = (self._session.query(Version)
                           .filter(Version.experiment_id == self.id)
                           .filter(Version.version == Version.DRAFT)
                           .scalar())

        if one_versoin:
            one_versoin.version = config['version']
            one_versoin.server_addr = config['server_addr']
            one_versoin.enabled_package = config['enabled_package']
            one_versoin.components = config['components']
        else:
            one_versoin = Version(
                version=config['version'],
                server_addr=config['server_addr'],
                enabled_package=config['enabled_package'],
                experiment_id=self.identity,
                components=config['components']
            )
            self._session.add(one_versoin)
        self._session.commit()
        return one_versoin.todict()

    def config_file(self, version):
        return self.experiment_dir / f'config.{str(version)}.json'

    def metadata_file(self):
        return self.experiment_dir / 'metadata.json'

    def runtime_config_file(self):
        return self.experiment_dir / 'runtime.config.json'

    def generate_runtime_config(self):
        """use metadata and current.config.json to generate a runtime.config.json
        file, which can be feed to featurize-runtime agent directly
        """
        runtime_config = self.get_metadata()
        config = self.get_config('current')
        dict_merge(runtime_config, config)
        update_json_file(self.runtime_config_file(), runtime_config)

    def commit_config(self):
        """Archived current version, publish draft version and create new draft
        version. Commit will also generate runtime config file
        """
        draft = self.config_file('draft')
        current = self.config_file('current')
        metadata = self.get_metadata()

        draft_config = self.get_config('draft')

        if os.path.isfile(current):
            # if has current, archived it
            current_config = self.get_config('current')
            shutil.move(current, self.config_file(current_config['version']))

        # make the draft version as the current
        shutil.copy(draft, current)

        # create a new draft version similar to the current,
        # except the version number should plus onek
        draft_config['version'] += 1
        self.update_config(draft_config)

        # update metadata
        metadata['total_versions'] += 1
        self.update_metadata(metadata)

    def update_metadata(self, metadata):
        update_json_file(self.metadata_file(), metadata)

    def get_metadata(self):
        one_experiment = (self._session.query(Experiment)
                              .filter(Experiment.id == self.id)
                              .scalar())
        return one_experiment.todict()

    def get_config(self, version):
        one_versoin = (self._session.query(Version)
                           .filter(Version.experiment_id == self.id)
                           .filter(Version.version==Version.DRAFT)
                           .scalar())
        return one_versoin.todict()

    def log_file(self):
        return self.experiment_dir / 'log.txt'

    def get_experiment(self, experiment_id=''):
        experiments = []
        if experiment_id == '':
            for one_experiment in self._session.query(Experiment).all():
                experiments.append(one_experiment.todict())
        else:
            one_experiment = self._session.query(Experiment).filter(Experiment.id == experiment_id).scalar()
            experiments.append(one_experiment.todict())
        self._session.commit()
        return experiments

    def add_experiment(self, experiment):
        package = PackageManager()
        experiment = Experiment(
            name=experiment['name'],
            enabled_packages=','.join(package.packages)
        )

        self._session.add(experiment)
        self._session.commit()
        self.prepare_directories()

    def update_experiment(self, experiemnt):
        one_experiment = self._session.query(Experiment).filter(Experiment.id == self.id).scalar()
        one_experiment.name = experiemnt['name']
        one_experiment.enabled_packages = experiemnt['enabled_packages']
        self._session.commit()

    def delete_experiment(self):
        one_experiment = (self._session.query(Experiment)
                              .filter(Experiment.id == self.id)
                              .scalar())
        relate_executions = (self._session.query(Execution)
                                 .filter(Execution.experiment_id == self.id)
                                 .all())
        if relate_executions != []:
            for one_execution in relate_executions:
                self._session.delete(one_execution)
        relate_modules = self._session.query(Module).filter(Module.experiment_id == self.id).all()
        if relate_modules != []:
            for one_module in relate_modules:
                self._session.delete(one_module)
        self._session.delete(one_experiment)
        self._session.commit()

    def add_remark(self, remark):
        metadata = self.get_metadata()
        if 'remarks' not in metadata:
            metadata['remarks'] = []
        metadata['remarks'].insert(0, remark)
        self.update_metadata(metadata)

    def get_execution(self, execution_id=''):
        executions = []
        if execution_id == '':
            for one_execution in self._session.query(Execution).filter(Execution.experiment_id == self.id).all():
                executions.append(one_execution.todict())
        else:
            one_execution = self._session.query(Execution).filter(Execution.id == execution_id).filter(Execution.experiment_id == self.id).scalar()
            executions.append(one_execution.todict())
        self._session.commit()
        return executions

    def add_execution(self, execution):
        execution = Execution(
            status=Execution.Status.not_running,
            task_type=execution['task_type'],
            agent_config=execution['agent_config'],
            experiment_id=self.id
        )
        self._session.add(execution)
        self._session.commit()
        return execution

    def update_execution(self, execution_id, execution):
        one_execution = self._session.query(Execution).filter(Execution.id == execution_id).filter(Execution.experiment_id == self.id).scalar()
        one_execution.status = execution['status']
        one_execution.task_type = execution['task_type']
        one_execution.agent_config = execution['agent_config']
        self._session.commit()

    def delete_execution(self, execution_id):
        one_execution = self._session.query(Execution).filter(Execution.id == execution_id).filter(Execution.experiment_id == self.id).scalar()
        self._session.delete(one_execution)
        self._session.commit()

    def get_module(self, module_id=''):
        modules = []
        if module_id == '':
            for one_module in self._session.query(Module).filter(Module.experiment_id == self.id).all():
                modules.append(one_module.todict())
        else:
            one_module = self._session.query(Module).filter(Module.id == module_id).filter(Module.experiment_id == self.id).scalar()
            modules.append(one_module.todict())
        self._session.commit()
        return modules

    def add_module(self, module):
        module = Module(
            name=module['name'],
            config=module['config'],
            experiment_id=self.id
        )
        self._session.add(module)
        self._session.commit()
        return module

    def update_module(self, module_id, module_dict):
        module = self._session.query(Module).filter(Module.id == module_id).filter(Module.experiment_id == self.id).scalar()
        module.name = module_dict['name']
        module.config = module_dict['config']
        self._session.commit()
        return module

    def delete_module(self, module_id):
        module = self._session.query(Module).filter(Module.id == module_id).filter(Module.experiment_id == self.id).scalar()
        self._session.delete(module)
        self._session.commit()

    def docker_file(self):
        return self.experiment_dir / 'docker.tar.gz'

    def create_docker_zip_file(self):
        dirpath = Path(tempfile.mkdtemp())
        requirements_file = dirpath / 'requirements.txt'
        runtime_file = dirpath / 'runtime.config.json'
        docker_file = dirpath / 'Dockerfile'

        with open(requirements_file, 'w') as f:
            content = "\n".join([
                'featurize-jupyterlab',
                'featurize-runtime',
                'featurize-package'
            ])
            f.write(content)

        with open(docker_file, 'w') as f:
            content = "\n".join([
                'FROM python:3',
                'WORKDIR /runtime',
                'COPY requirements.txt /runtime',
                'RUN pip3 install -r requirements.txt',
                'COPY . /runtime',
                'RUN featurize_server package:add ftpkg.demo',
                'CMD featurize run --config runtime.config.json',
            ])
            f.write(content)
        shutil.copy(self.runtime_config_file(), runtime_file)
        make_tarfile(self.docker_file(), dirpath)
        return dirpath


class Comment(BaseModel, BaseORM):
    __tablename__ = 'comments'

    content = Column(String)
    commentable_id = Column(UUID(as_uuid=True), unique=False, nullable=False)
    commentable_type = Column(String)


execution_module_associations = Table(
    'execution_module_associations',
    BaseORM.metadata,
    Column('execution_id', UUID, ForeignKey('executions.id'), primary_key=True),
    Column('module_id', UUID, ForeignKey('modules.id'), primary_key=True)
)


class Execution(BaseModel, BaseORM):

    class Status(enum.Enum):
        running = 'running'
        idle = 'idle'
        error = 'error'
        not_running = 'not_running'
        booting = 'booting'
        starting = 'starting'
        stopping = 'stopping'
        killing = 'killing'

    __tablename__ = 'executions'

    status = Column(Enum(Status), default=Status.not_running)
    task_type = Column(String)
    agent_config = Column(JSON)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey('experiments.id'), unique=False, nullable=False)
    modules = relationship("Module", back_populates="executions", secondary=execution_module_associations)

    def todict(self):
        one_dict = {}
        one_dict['id'] = str(self.id)
        one_dict['created_at'] = self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        one_dict['updated_at'] = self.updated_at.strftime("%d/%m/%Y %H:%M:%S")
        one_dict['status'] = self.status.value
        one_dict['task_type'] = self.task_type
        one_dict['agent_config'] = self.agent_config
        one_dict['experiment_id'] = str(self.experiment_id)
        return one_dict

    def generate_config(self):
        config = {
            'identity': str(self.id),
            'task': self.task_type,
            'modules': {},
            'options': {},
            'agent_config': self.agent_config,
            'server_addr': f'{Config.server_addr}:{Config.rpc_port}',
            'enabled_package': PackageManager().packages
        }
        for module in self.modules:
            config['modules'][module.key] = module.todict()
        with open(self.config_file(), 'w') as f:
            json.dump(config, f)

    def config_file(self):
        return self.dir() / 'config.json'

    def log_file(self):
        return self.dir() / 'log.txt'

    def dir(self):
        return self.experiment.dir() / str(self.id)

    def prepare_directories(self):
        try:
            os.makedirs(self.dir())
        except FileExistsError:
            pass

    def graph_file(self, graph_name):
        return self.dir() / f"graph__{graph_name}"

    def create_graph(self, graph_name):
        self.graph_file(graph_name).touch()

    def get_graphs(self):
        return list(filter(lambda x: x[0:7] == 'graph__', os.listdir(self.dir())))

    def add_point(self, graph_name, point):
        graph_file = self.graph_file(graph_name)
        raw_point = minetorch_pb2.RawPoint()
        raw_point.x = point['x']
        raw_point.y = point['y']
        with open(graph_file, 'ab') as f:
            stream.dump(f, raw_point, gzip=False)


Index('execution_experiment_id_index', Execution.experiment_id)


class Module(BaseModel, BaseORM):
    __tablename__ = "modules"

    name = Column(String)
    key = Column(String)
    config = Column(JSON)
    experiment_id = Column(UUID(as_uuid=True), unique=False, nullable=False)
    executions = relationship("Execution", back_populates="modules", secondary=execution_module_associations)

    def todict(self):
        one_dict = {}
        one_dict['id'] = str(self.id)
        one_dict['created_at'] = self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        one_dict['updated_at'] = self.updated_at.strftime("%d/%m/%Y %H:%M:%S")
        one_dict['name'] = self.name
        one_dict['key'] = self.key
        one_dict['config'] = self.config
        one_dict['experiment_id'] = str(self.experiment_id)
        return one_dict


Index('module_experiment_id_index', Module.experiment_id)
