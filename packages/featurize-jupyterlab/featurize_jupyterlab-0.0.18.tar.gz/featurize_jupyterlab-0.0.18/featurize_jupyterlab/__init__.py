from . import core
from .handlers import setup_handlers
from .proto import minetorch_pb2
from .proto import minetorch_pb2_grpc
from . import constants
from .package_manager import package_manager
from .cli import cli
from .transform import DualImageTransformation


def _jupyter_server_extension_paths():
    return [{"module": "featurize_jupyterlab"}]


def load_jupyter_server_extension(nb_server_app):
    core.boot()
    setup_handlers(nb_server_app)


__all__ = ['minetorch_pb2', 'minetorch_pb2_grpc', 'constants', 'package_manager', 'cli', 'DualImageTransformation']
