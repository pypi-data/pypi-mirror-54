import logging

from productfeeds.importers.base import AbstractImporter
from productfeeds.storage.base import AbstractStorage
from productfeeds.utils import load_custom_library, import_libraries

IMPORTERS = import_libraries('importer')
STORAGES = import_libraries('storage')

logger = logging.getLogger(__name__)


class APILoaderError(Exception):
    pass


def build_importer(importer, config, storage=None, tmp_dir=""):
    """
    Instantiate importer object by given settings
    Args:
        importer (str): Importer name
        config (dict): Importer settings
        storage (storage.AbstractStorage): Storage object
    Return:
        importers (ImporterAbstractAPI): The importer API object
    Raises:
        None
    """
    try:
        return IMPORTERS[importer](storage=storage, tmp_dir=tmp_dir, **config)
    except KeyError:
        if ':' in importer:
            importer_class = IMPORTERS[importer] = load_custom_library(importer)
            importer_obj = importer_class(storage=storage, tmp_dir=tmp_dir, **config)
            if not isinstance(importer_obj, AbstractImporter):
                raise APILoaderError(
                    '{} should inherit interface of {}'.format(
                        importer_class,
                        'productfeeds.importers.AbstractImporterAPI'
                    )
                )
            return importer_obj
        else:
            raise


def build_storage(storage, config):
    try:
        return STORAGES[storage](config)
    except KeyError:
        if ':' in storage:
            storage_class = STORAGES[storage] = load_custom_library(storage)
            storage_obj = storage_class(config)
            if not isinstance(storage_obj, AbstractStorage):
                raise APILoaderError(
                    '{} should inherit interface of {}'.format(storage_class, 'productfeeds.storage.AbstractStorage')
                )
            return storage_obj
        else:
            raise


def import_feeds(source_config, destination_config, tmp_dir=''):
    storage = None
    if destination_config and 'storage' in destination_config:
        storage = build_storage(
            destination_config['storage'],
            destination_config['config'] if 'config' in destination_config else None
        )
        storage.clear()

    for importer in source_config:
        logger.info('Importing feeds from %s', importer['api'])
        api = build_importer(importer['api'], importer['config'], storage=storage, tmp_dir=tmp_dir)
        result = api.import_products()
        logger.info("%s Imported and %s skipped products.", api.saved_products_count, api.skipped_products_count)
