import json
import humps
from datetime import datetime

import stream
from notebook.base.handlers import APIHandler, web
from notebook.utils import url_path_join as ujoin

from sqlalchemy.orm import sessionmaker

from . import core
from .models import Experiment, Execution, Module
from .package_manager import PackageManager
from .proto import minetorch_pb2
from .config import Config


class FeaturizeHandler(APIHandler):

    def finish(self, data={}):
        wrapped_data = {
            'status': 'success',
            'data': data,
        }
        return super().finish(json.dumps(humps.camelize(wrapped_data)))

    def prepare(self):
        self.experiment = None
        self.post_data = None
        self.session = sessionmaker(bind=Config.engine)()

        if self.request.method == 'POST' or self.request.method == 'PUT':
            self.post_data = humps.decamelize(json.loads(self.request.body))
            identity = self.post_data.get('identity', self.path_kwargs.get('identity', None))
        else:
            identity = self.get_argument('identity', self.path_kwargs.get('identity', None))

        if identity is not None:
            self.experiment = Experiment(_session=self.session, id=identity)
        else:
            self.experiment = Experiment(_session=self.session)

class CommitmentHandler(FeaturizeHandler):

    def post(self):
        self.experiment.commit_config()
        self.experiment.generate_runtime_config()
        self.experiment.create_docker_zip_file()
        self.finish()


class DockerfileHandler(web.RequestHandler):

    def get(self):
        identity = self.get_argument('identity', None)
        if identity is None:
            self.set_status(400)
            self.finish()
            return
        experiment = Experiment(identity)

        self.set_header("Content-Disposition", "attachment; filename=docker.tar.gz")
        with open(experiment.docker_file(), 'rb') as f:
            while 1:
                data = f.read(16384)  # or some other nice-sized chunk
                if not data:
                    break
                self.write(data)
        self.finish()


class ExperimentsHandler(FeaturizeHandler):

    def post(self):
        self.experiment.add_experiment(self.post_data)
        self.finish()

    def get(self):
        experiments = self.experiment.get_experiment()
        self.finish(experiments)


class ExperimentHandler(FeaturizeHandler):

    def get(self, identity):
        one_experiment = self.experiment.get_experiment(identity)
        self.finish(one_experiment)

    def put(self, identity):
        self.experiment.update_experiment(self.post_data)
        self.finish()

    def delete(self, identity):
        self.experiment.delete_experiment()
        self.finish()
    

class ComponentsHandler(FeaturizeHandler):

    def get(self, identity):
        components = core.registed_components()
        data = list(map(lambda m: m.to_json_serializable(), components))
        self.finish(data)


class ConfigHandler(FeaturizeHandler):

    def get(self):
        one_version_dict = self.experiment.get_config('draft')
        self.finish(one_version_dict)

    def post(self):
        data = json.loads(self.request.body)
        version_post_dict = self.experiment.update_config(data['config'])
        self.finish(version_post_dict)


class ExperimentStatusHandler(FeaturizeHandler):

    def post(self):
        self.experiment.update_metadata({
            'status': self.post_data['status']
        })


class ExperimentGraphHandler(FeaturizeHandler):

    def get(self):
        graph_name = self.get_argument('graph_name', None)
        start_at = int(self.get_argument('start_at', 0))

        with open(self.experiment.graph_file(graph_name), 'rb') as f:
            f.seek(start_at)
            points = [a for a in stream.parse(f, minetorch_pb2.Point)]
            points = list(map(lambda p: {'x': p.x, 'y': p.y}, points))
            self.finish({
                'position': f.tell(),
                'points': points,
            })


class LogHandler(FeaturizeHandler):

    def get(self):
        offset = int(self.get_argument('offset', 0))
        limit = int(self.get_argument('limit', 1000))

        with open(self.experiment.log_file(), 'r') as f:
            f.seek(offset)
            content = f.read(limit)
            while True:
                char = f.read(1)
                if char and char != "\n":
                    content += char
                else:
                    break
            self.finish({
                'read_up_to': f.tell(),
                'logs': content,
            })


class RemarkHandler(FeaturizeHandler):

    def post(self):
        self.experiment.add_remark(self.post_data['remark'])
        self.finish()


class ExecutionsHandler(FeaturizeHandler):

    def post(self, identity):
        self.experiment.add_execution(self.post_data)
        self.finish()

    def get(self, identity):
        executions = self.experiment.get_execution()
        self.finish(executions)


class ExecutionHandler(FeaturizeHandler):

    def get(self, identity, execution_identity):
        execution_identity = self.get_argument('execution_identity', self.path_kwargs.get('execution_identity', None))
        execution = self.experiment.get_execution(execution_identity)
        self.finish(execution)

    def put(self, identity, execution_identity):
        execution_identity = self.get_argument('execution_identity', self.path_kwargs.get('execution_identity', None))
        execution = self.experiment.update_execution(execution_identity, self.post_data)
        self.finish()
    
    def delete(self, identity, execution_identity):
        execution_identity = self.get_argument('execution_identity', self.path_kwargs.get('execution_identity', None))
        self.experiment.delete_execution(execution_identity)
        self.finish()


class ModulesHandler(FeaturizeHandler):

    def get(self, identity):
        modules = self.experiment.get_module()
        self.finish(modules)

    def post(self, identity):
        self.experiment.add_module(self.post_data)
        self.finish()


class ModuleHandler(FeaturizeHandler):

    def put(self, identity, module_identity):
        module_identity = self.get_argument('module_identity', self.path_kwargs.get('module_identity', None))
        module = self.experiment.update_module(module_identity, self.post_data)
        self.finish()
    
    def delete(self, identity, module_identity):
        module_identity = self.get_argument('module_identity', self.path_kwargs.get('module_identity', None))
        self.experiment.delete_module(module_identity)
        self.finish()


def setup_handlers(npapp):
    featurize_handlers = [
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/components", ComponentsHandler),

        ("/featurize/config", ConfigHandler),
        ("/featurize/experiments/status", ExperimentStatusHandler),
        ("/featurize/commitment", CommitmentHandler),
        ("/featurize/experiments/graphs", ExperimentGraphHandler),
        ("/featurize/experiments/log", LogHandler),
        ("/featurize/experiments/remark", RemarkHandler),
        ("/featurize/experiments/dockerfile", DockerfileHandler),

        ("/featurize/experiments", ExperimentsHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)", ExperimentHandler),


        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/executions", ExecutionsHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/executions/(?P<execution_identity>[\w\d\-]+)", ExecutionHandler),

        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/modules", ModulesHandler),
        (r"/featurize/experiments/(?P<identity>[\w\d\-]+)/modules/(?P<module_identity>[\w\d\-]+)", ModuleHandler)
    ]

    # add the baseurl to our paths
    base_url = npapp.web_app.settings["base_url"]
    featurize_handlers = [(ujoin(base_url, x[0]), x[1]) for x in featurize_handlers]
    npapp.web_app.add_handlers(".*", featurize_handlers)
