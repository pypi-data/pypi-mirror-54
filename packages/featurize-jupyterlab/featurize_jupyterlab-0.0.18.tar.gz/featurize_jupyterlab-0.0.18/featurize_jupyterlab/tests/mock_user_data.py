from featurize_jupyterlab.models import Experiment, Module, Execution, Comment
from featurize_jupyterlab.config import Config
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=Config.engine)()

experiment = Experiment(name='Mine Experiment')
session.add(experiment)
session.flush()

modules = [
    Module(name='Train DataLoader', experiment_id=experiment.id),
    Module(name='Val Dataloader', experiment_id=experiment.id)
]

execution = Execution(status='not_running', task_type='train', experiment_id=experiment.id)

comments = [
    Comment(content='test comment 1', commentable_id=experiment.id, commentable_type='Experiment'),
    Comment(content='test comment 2', commentable_id=experiment.id, commentable_type='Experiment')
]


session.bulk_save_objects(modules)
session.add(execution)
session.bulk_save_objects(comments)
session.flush()

comments_two = [
    Comment(content='test comment 3', commentable_id=execution.id, commentable_type='Execution'),
    Comment(content='test comment 4', commentable_id=execution.id, commentable_type='Execution')
]
session.bulk_save_objects(comments_two)

experiments = [
    Experiment(name='Mine Experiment2'),
    Experiment(name='Mine Experiment3')
]
session.bulk_save_objects(experiments)

session.commit()
