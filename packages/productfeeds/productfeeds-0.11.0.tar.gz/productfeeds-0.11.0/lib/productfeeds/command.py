from __future__ import print_function
import logging
import argparse
import yaml
from .base import import_feeds as import_feeds_to_storage


def import_feeds():
    """
    Shell command `productfeed-import` which imports feeds based on YAML configuration
    config_file (shell argument): Config file (YAML) path

    Config file example:

    tmp_dir: "/home/myuser/tmp"
    source:
      - importers: "convertiser"
        config:
          token: "__MY_SECRET_TOKEN__"
          website_key: "__MY_SECRET_WEBSITE_KEY__"
          offers:
            - MY_OFFER_ID
            - ANOTHER_OFFER_ID

      - importers: "webepartners"
        config:
          login: "MY_LOGIN"
          password: "MY_PASSWORD"

      - importers: "mycustom_module:MyCustomImporterClass"
        config:
          my_custom: "settings"

      - importers: "./my_dir/mycustom_module_file.py:MyCustomImporterClass"
        config:
          my_custom: "settings"

    destination:
      storage: 'mysql'
      config:
        host: 'MY_HOST'
        user: 'MY_USERNAME'
        passwd: 'MY_PASSWORD'
        db: 'MY_DATABASE'
        table: 'MY_TABLE'
    """
    logger_handler = logging.StreamHandler()  # Handler for the logger
    logger_handler.setFormatter(logging.Formatter('%(levelname)s [%(name)s:%(lineno)s] %(message)s'))
    logger = logging.getLogger()
    logger.addHandler(logger_handler)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='config YAML file')
    args = parser.parse_args()
    with open(args.config_file, "r") as stream:
        settings = yaml.load(stream, Loader=yaml.SafeLoader)
    try:
        tmp_dir = settings['tmp_dir']
    except KeyError:
        tmp_dir = ''
    importers = settings['source']
    logger.info('Importers settings: %s', importers)
    logger.info('Destination settings: %s', settings['destination'])
    import_feeds_to_storage(settings['source'], settings['destination'], tmp_dir=tmp_dir)
    #FIXME Exceptions handling
