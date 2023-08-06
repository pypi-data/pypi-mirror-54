from .models import Experiment, Module
from .utils import create_session


def main():
    session = create_session()

    experiment = Experiment(name='demo', _session=session)
    session.add(experiment)
    session.flush()

    experiment.prepare_directories()

    train_dataloader = Module(key='train_dataloader', experiment_id=experiment.id, config=[])
    val_dataloader = Module(key='val_dataloader', experiment_id=experiment.id, config=[])
    dataset = Module(key='dataset', experiment_id=experiment.id, config=[{
        'type': 'Dataset',
        'name': 'MNISTDataset',
        'parameters': {
            'fold': '/tmp/data'
        }
    }])
    model = Module(key='model', experiment_id=experiment.id, config=[{
        'type': 'Model',
        'name': 'SmallModel'
    }])
    loss = Module(key='loss', experiment_id=experiment.id, config=[{
        'type': 'Loss',
        'name': 'NllLoss'
    }])
    optimizer = Module(key='optimizer', experiment_id=experiment.id, config=[{
        'type': 'Optimizer',
        'name': 'PyTorchSGD'
    }])

    session.add(train_dataloader)
    session.add(val_dataloader)
    session.add(dataset)
    session.add(model)
    session.add(loss)
    session.add(optimizer)

    execution = experiment.add_execution({
        'task_type': 'Minetorch',
        'agent_config': {}
    })

    execution.modules.append(train_dataloader)
    execution.modules.append(val_dataloader)
    execution.modules.append(dataset)
    execution.modules.append(model)
    execution.modules.append(loss)
    execution.modules.append(optimizer)

    execution.prepare_directories()
    execution.generate_config()
