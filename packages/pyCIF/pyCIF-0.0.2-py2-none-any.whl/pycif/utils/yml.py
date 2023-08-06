import yaml
from collections import OrderedDict


def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    """A function from Stack-OverFlow to keep the order of lines in the Yaml.
    See: https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts"""

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)
