from featurize_jupyterlab.models import Experiment
from featurize_jupyterlab.config import Config
from sqlalchemy.orm import sessionmaker
import pytest


@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called.")
    request.addfinalizer(teardown_module)
    print('setup_module called.')


# def test_1(setup_module):
#     print("test_1 beign")
#     session = sessionmaker(Config.engine)()

#     experiment = Experiment(
#         _session=session,
#         id='3053d58a-fc6d-4546-83fb-dc0622bff1c4'
#     )
#     # execution = {
#     #     'task_type': 'train',
#     #     'agent_config': {}
#     # }
#     # experiment.add_execution(execution)
#     module = {
#         'name': 'test_module',
#         'config': {}
#     }
#     experiment.add_module(module)
#     print("test_1 end")
