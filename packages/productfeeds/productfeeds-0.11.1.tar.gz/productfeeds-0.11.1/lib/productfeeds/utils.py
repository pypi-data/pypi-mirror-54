import glob
import imp
import importlib
import ntpath
from os.path import dirname


IMPORTS_SETTINGS = {
    'importer': {
        'directory': 'importers',
        'module_suffix': 'api',
        'class_suffix': 'Importer',
    },
    'storage': {
        'directory': 'storage',
        'module_suffix': 'storage',
        'class_suffix': 'Storage',
    }
}
__MODULES_TO_LOAD = {'importer': [], 'storage': []}
for importer_type, importer_settings in IMPORTS_SETTINGS.items():
    __MODULES_TO_LOAD[importer_type] += [
        ntpath.basename(file_path).replace(".py", "")
        for file_path in glob.glob(
            dirname(__file__) + "/{}/*{}.py".format(importer_settings['directory'], importer_settings['module_suffix'])
        )
    ]


def load_custom_library(module_and_class):
    my_module, my_class = module_and_class.split(':')
    try:
        my_module_object = importlib.import_module(my_module)
    except TypeError:
        my_module_object = imp.load_source("mymodule", my_module)
        my_class_object = getattr(my_module_object, my_class)
    else:
        my_class_object = getattr(my_module_object, my_class)

    return my_class_object


def import_libraries(library_type):
    libraries = {}
    class_suffix = IMPORTS_SETTINGS[library_type]['class_suffix']

    for my_module in __MODULES_TO_LOAD[library_type]:
        module_path = "productfeeds.{}.{}".format(IMPORTS_SETTINGS[library_type]['directory'], my_module)
        my_module_object = importlib.import_module(module_path)
        for attribute in dir(my_module_object):
            if attribute[-len(class_suffix):] == class_suffix and attribute != 'Abstract{}'.format(class_suffix):
                storage_code = str.lower(attribute[:-len(class_suffix)])
                libraries[storage_code] = getattr(my_module_object, attribute)
    return libraries

