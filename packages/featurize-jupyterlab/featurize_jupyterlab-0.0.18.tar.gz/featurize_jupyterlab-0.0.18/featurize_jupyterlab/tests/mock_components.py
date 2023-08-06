from featurize_jupyterlab.core import Component, Dataset, Dataflow, Option, Task, Module
from featurize_jupyterlab.transform import BasicImageTransformation, DualImageTransformation
from albumentations import RandomBrightnessContrast, RandomCrop


class RealComponent(Component):
    """This is a real component
    """
    def __call__(self):
        pass


class SomeDatasetComponent(Dataset):
    """This is a dataset component
    """
    name = 'Name overrided'
    description = 'This is a overrided description'

    def __call__(self):
        pass


class AbstractComponent(Component):
    """if a component has no __call__ method, then it
    is an abstract component
    """
    pass


class OptionComponent(Dataflow):
    """A component with options
    """
    batch_size = Option(name='Batch Size', type='number', default=1)
    epochs = Option(type='number', default=4)
    remark = Option()
    metadata = {
        'banner': 'banner_url'
    }

    def __call__(self):
        return {
            'a': self.batch_size,
            'b': self.epochs,
            'c': self.remark
        }


class Brightness(BasicImageTransformation):
    """Add a fixed integer to all pixels of an image
    """
    brightness_limit = Option(type='number', default=0.2)
    contrast_limit = Option(type='number', default=0.2)
    brightness_by_max = Option(type='number')
    columns_config = Option(type='string')

    def create_aug(self):
        return RandomBrightnessContrast(
            self.brightness_limit,
            self.contrast_limit,
            self.brightness_by_max,
            p=self.probability
        )


class Crop(DualImageTransformation):
    """Apply random crop to images
    """
    columns_config = Option(type='string')
    width = Option(type='number')
    height = Option(type='number')

    def create_aug(self):
        return RandomCrop(self.height, self.width, p=self.probability)


class TestTask(Task):
    """This is a task
    """
    param1 = Option(type='string')
    param2 = Option(type='string')

    module1 = Module(component_types=['Dataflow'])
    module2 = Module(component_types=['Dataset'], name='name of module 2', required=True)

    def __call__(self):
        pass


class AnotherTestTask(Task):
    name = 'Test Task 2'
    description = 'This is another task'

    def __call__(self):
        pass
