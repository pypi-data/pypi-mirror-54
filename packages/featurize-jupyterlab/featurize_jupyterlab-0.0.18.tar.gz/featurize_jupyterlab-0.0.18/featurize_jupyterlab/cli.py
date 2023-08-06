import subprocess
import sys
from pathlib import Path
from .config import Config

import click

PYTHON_INTERPRETER = 'python3'


@click.group()
def cli():
    pass


@cli.command('rpc:server')
def start_rpc_server():
    from .rpc_server import RpcServer
    server = RpcServer(10, f"{Config.server_addr}:{Config.rpc_port}")
    server.serve()


@cli.command('proto:compile')
def proto_compile():
    minetorch_dir = Path(__file__).resolve().parents[1]
    proto_dir = Path('featurize_jupyterlab') / 'proto'
    subprocess.Popen([
        PYTHON_INTERPRETER,
        "-m",
        "grpc_tools.protoc",
        f"-I.",
        f"--python_out=.",
        f"--grpc_python_out=.",
        f"{proto_dir / 'minetorch.proto'}"
    ], stdout=sys.stdout, cwd=minetorch_dir)


@cli.command('package:add')
@click.argument('package')
def add_package(package):
    from .package_manager import package_manager
    package_manager.add_package(package)


@cli.command('component:list')
def component_list():
    from . import core
    core.boot()
    print("\n".join(list(map(lambda x: x.name, core.registed_components()))))


@cli.command('package:remove')
@click.argument('package')
def remove_package(package):
    from .package_manager import package_manager
    package_manager.remove_package(package)


@cli.command('package:list')
def list_packages():
    from .package_manager import package_manager
    package_manager.list_packages()


@cli.command('db:init')
@click.argument('dropdb', default=False)
def init_database(dropdb=False):
    from .models import BaseORM
    from .config import Config
    if dropdb:
        BaseORM.metadata.drop_all(Config.engine)
    BaseORM.metadata.create_all(Config.engine)


@cli.command('db:seed')
def db_seed():
    from . import seed
    seed.main()


@cli.command('db:drop')
def drop_database():
    from .models import BaseORM
    from .config import Config
    BaseORM.metadata.drop_all(Config.engine)


@cli.command('db:reset')
def reset_database():
    from .models import BaseORM
    from .config import Config
    BaseORM.metadata.drop_all(Config.engine)
    BaseORM.metadata.create_all(Config.engine)


@cli.command('run')
@click.option('--config', help='Absolute path of the config file', required=True)
def runtime_run(config):
    from .task.process import main_process
    main_process(config)


def main():
    cli()


if __name__ == '__main__':
    main()
