from . import constants as C
from .logger import get_runtime_logger

from .proto import minetorch_pb2, minetorch_pb2_grpc
from .models import Execution
from sqlalchemy.orm import sessionmaker
from .config import Config


class MinetorchServicer(minetorch_pb2_grpc.MinetorchServicer):

    def __init__(self):
        self.session = sessionmaker(bind=Config.engine)()

    # TODO: performance of rpc server
    caches = {}

    def _get_execution(self, identity):
        return self.session.query(Execution).get(identity)

    def CreateGraph(self, request, context):
        # TODO: duplicate checking
        execution = self._get_execution(request.identity)
        execution.create_graph(request.graph_name)
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def AddPoint(self, request, context):
        # TODO: performance
        execution = self._get_execution(request.identity)
        execution.add_point(request.graph_name, {'x': request.x, 'y': request.y})
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def SendLog(self, request, context):
        # TODO: performance
        logger = get_runtime_logger(request.identity, self.session)
        getattr(logger, request.level.lower())(request.log)
        return minetorch_pb2.StandardResponse(
            status=0,
            message='ok'
        )

    def HeyYo(self, request, context):
        execution = self._get_execution(request.identity)
        agent_status = request.status
        server_status = getattr(C, f"status_{execution.status.value}".upper())

        # Priority of status: Server Verb status > agent_status > server_status
        # TODO: find a way to set the status as not_running
        if server_status == C.STATUS_STARTING and agent_status == C.STATUS_IDLE:
            command = C.COMMAND_RUN
        elif server_status == C.STATUS_STOPPING and agent_status == C.STATUS_RUNNING:
            command = C.COMMAND_HALT
        elif server_status == C.STATUS_KILLING and agent_status == C.STATUS_IDLE:
            command = C.COMMAND_KILL
        else:
            execution.status = getattr(Execution.Status, minetorch_pb2.HeyMessage.Status.Name(agent_status).lower()).value
            self.session.commit()
            command = C.COMMAND_NONE
        return minetorch_pb2.YoMessage(
            roger=True,
            command=command
        )
