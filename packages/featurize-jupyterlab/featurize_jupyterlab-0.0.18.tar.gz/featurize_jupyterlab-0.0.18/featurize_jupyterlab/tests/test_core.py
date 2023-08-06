from featurize_jupyterlab import core
import json
from . import mock_components as mock


def test_component_metainfo():
    assert mock.RealComponent.name == 'RealComponent'
    assert mock.RealComponent.description == 'This is a real component'
    assert mock.RealComponent.meta == core.ComponentMeta

    assert mock.SomeDatasetComponent.name == 'Name overrided'
    assert mock.SomeDatasetComponent.description == 'This is a overrided description'
    assert mock.SomeDatasetComponent.meta == core.ComponentMeta


def test_registed_components():
    assert core.ComponentMeta.registed_components[0] == mock.RealComponent
    assert core.ComponentMeta.registed_components[1] == mock.SomeDatasetComponent
    assert core.ComponentMeta.registed_components[2] == mock.OptionComponent


def test_options():
    assert len(mock.RealComponent.options) == 0
    assert len(mock.OptionComponent.options) == 3
    assert mock.OptionComponent.options[0].key == 'batch_size'
    assert mock.OptionComponent.options[0].name == 'Batch Size'
    assert mock.OptionComponent.options[0].type == 'number'
    assert mock.OptionComponent.options[0].required

    assert mock.OptionComponent.options[1].key == 'epochs'
    assert mock.OptionComponent.options[1].name == 'epochs'
    assert mock.OptionComponent.options[1].type == 'number'
    assert mock.OptionComponent.options[1].default == 4

    assert mock.OptionComponent.options[2].type == 'string'


def test_formalize_component():
    user_settings = {'batch_size': 123, 'epochs': 321, 'remark': 'this is remark'}
    option = mock.OptionComponent(**user_settings)
    result = option()

    assert result['a'] == 123
    assert result['b'] == 321
    assert result['c'] == 'this is remark'


def test_component_serialize():
    result = mock.OptionComponent.to_json_serializable()
    assert result['name'] == 'OptionComponent'
    assert result['description'] == 'A component with options'
    assert result['metadata']['banner'] == 'banner_url'
    assert result['options'][0]['key'] == 'batch_size'


def test_component_type():
    class AnotherOptionComponent(mock.OptionComponent):
        pass

    assert mock.RealComponent.component_type is None
    assert mock.SomeDatasetComponent.component_type == 'Dataset'
    assert mock.AbstractComponent.component_type is None
    assert mock.OptionComponent.component_type == 'Dataflow'
    assert AnotherOptionComponent.component_type == 'Dataflow'


def test_option_post_process():
    class OptionCallbackCompbonent(core.Dataflow):
        """A component with a callback option
        """
        some_json_string = core.Option(type='string', default=1, post_process=lambda x: json.loads(x))

        def __call__(self):
            return self.some_json_string

    component = OptionCallbackCompbonent(some_json_string='{"xxx": "yyy"}')
    result = component()
    assert "xxx" in result
    assert result["xxx"] == "yyy"


def test_task_option():
    assert len(mock.TestTask.options) == 2
    assert mock.TestTask.options[0].key == 'param1'


def test_task_module():
    assert len(mock.TestTask.modules) == 2
    assert mock.TestTask.modules[0].key == 'module1'
    assert mock.TestTask.modules[0].to_json_serializable()['key'] == 'module1'
