from . import core
from . import process_env as env
from . import g
from .plugins import Plugin
from minetorch import Trainer
import torch


def init_component(component_type, component_config):
    component_name = component_config['name']
    component_settings = component_config['settings']
    if component_type[-1] == 's':
        plural_component_cls_name = f'{component_type}es'
    else:
        plural_component_cls_name = f'{component_type}s'
    register_components = getattr(getattr(core, component_type), f'registed_{plural_component_cls_name}')
    component = next((component for component in register_components if component.name == component_name), None)
    return component.func(**component_settings)


def main(config_file):
    core.boot()
    env.init_process_env(config_file)

    g.dataset = init_component('dataset', env.config['dataset'])
    g.dataloader = torch.utils.data.DataLoader(g.dataset, batch_size=256, shuffle=True)
    # dataflow = init_component('dataflow', env.config['dataflow'])
    g.model = init_component('model', env.config['model'])
    g.optimizer = init_component('optimizer', env.config['optimizer'])
    g.loss = init_component('loss', env.config['loss'])

    trainer = Trainer(
        alchemistic_directory='./log',
        model=g.model,
        optimizer=g.optimizer,
        train_dataloader=g.dataloader,
        loss_func=g.loss,
        plugins=Plugin.registed_plugins
    )

    try:
        trainer.train()
    except Exception as e:
        env.logger.error(f'unexpected error in training process: {e}')
