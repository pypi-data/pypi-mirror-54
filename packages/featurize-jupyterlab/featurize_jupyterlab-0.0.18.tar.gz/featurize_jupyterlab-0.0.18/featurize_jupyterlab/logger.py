import logging
from .models import Execution

runtime_loggers = {}


def get_runtime_logger(identity, session):
    global runtime_loggers
    logger_name = f'runtime_logger_{identity}'

    if logger_name in runtime_loggers:
        return runtime_loggers[logger_name]

    execution = session.query(Execution).get(identity)
    runtime_logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(execution.log_file())
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s', datefmt="%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    runtime_logger.addHandler(handler)
    runtime_logger.setLevel(logging.DEBUG)
    runtime_loggers[logger_name] = runtime_logger
    return runtime_logger
