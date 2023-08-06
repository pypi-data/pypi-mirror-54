import logging
import sys
import time
import unicodedata
try:
    import urllib.parse
except ImportError:
    import urllib
    urlencode_func = urllib.quote_plus
else:
    def urlencode_func(param):
        return urllib.parse.quote(param, safe='')
from abc import abstractmethod, ABCMeta

logger = logging.getLogger(__name__)


class AbstractImporterAPIException(Exception):
    pass


class ProductBuilderError(Exception):
    pass


class AbstractImporter:
    __metaclass__ = ABCMeta

    def __init__(self, articlecode_prefix='', *args, **kwargs):
        self.prefix = articlecode_prefix
        try:
            self.storage = kwargs['storage']
        except KeyError:
            self.storage = None

        self.prefix = articlecode_prefix
        self.filters = None
        if 'filters' in kwargs:
            self.filters = kwargs['filters']
        try:
            self.tmp_dir = kwargs['tmp_dir']
        except KeyError:
            self.tmp_dir = ''
        self.repeat_if_broken_fetching_count = 0
        if 'repeat_if_broken_fetching_count' in kwargs:
            self.repeat_if_broken_fetching_count = kwargs['repeat_if_broken_fetching_count']

        self.timeout_if_broken_fetching = 0
        if 'timeout_if_broken_fetching' in kwargs:
            self.timeout_if_broken_fetching = kwargs['timeout_if_broken_fetching']
        self.saved_products_count = 0
        self.skipped_products_count = 0

    @abstractmethod
    def get_feeds(self):
        pass

    @abstractmethod
    def _generate_feed_items(self, handler):
        pass

    @abstractmethod
    def _fetch(self, *args, **kwargs):
        pass

    @abstractmethod
    def _build_product(self, *args, **kwargs):
        pass

    def _build_articlecode(self, product_id):
        prefix = ''
        if self.prefix:
            prefix = self.prefix

        return "{}{}".format(prefix, product_id)

    @staticmethod
    def _slugify_filter(name):
        name = unicodedata.normalize('NFKD', name).\
                encode('ascii', 'ignore').lower().decode('utf-8')

        name = "{}".format(name)
        name = name.replace('.', '').strip()
        return name

    @staticmethod
    def _apply_filter_on_product(p, f):
        """
        This function allows to modify some fields of feed
        Args:
        p (Product) Product object
        f (dict) Transform settings
        """
        filters_map = {
            'title': str.title,
            'capitalize': str.title,
            'copy': str,
            'slugify': AbstractImporter._slugify_filter,
            'urlencode': urlencode_func,
            'join': "".join,
        }
        filter_function_and_params = f['filter']
        if not isinstance(filter_function_and_params, list):
            filter_function_and_params = f['filter'].split(':')
        func_name = filter_function_and_params[0]
        params = filter_function_and_params[1:]
        if params:
            param_list = []
            for param in params:
                if param.startswith('$'):
                    value = p.d[param[1:]]
                else:
                    value = param
                param_list.append(value)
            if len(param_list) == 1:
                param_list = param_list[0]

            # if sys.version_info[0] < 3:
            #     value = value.decode('utf-8')
            func = filters_map[func_name]
            try:
                f_result = func(param_list)
            except:
                pass
            else:
                p.d[f['field']] = f_result

    def _read_data(self, *args, **kwargs):
        """
        Fetching data with repeating if something goes wrong
        """
        results = None
        repeat_if_broken_count = self.repeat_if_broken_fetching_count
        while repeat_if_broken_count > -1:
            repeat_if_broken_count -= 1
            try:
                results = self._fetch(*args, **kwargs)
            except Exception as e:
                logger.warn('[Fetching data {} {}] Repeat in {} seconds because of: {}'.format(
                    args, kwargs, self.timeout_if_broken_fetching, e
                ))

                if repeat_if_broken_count == -1:
                    raise
                time.sleep(self.timeout_if_broken_fetching)
            else:
                break
        return results

    def import_products(self):
        rs = {'status': 1}
        feeds = self.get_feeds()
        feeds_count = len(feeds)
        imported_feeds = 0
        for feed in feeds:
            logger.info('Importing feed %s', feed)
            feed_handler = self._read_data(feed)
            imported_products = 0
            for item in self._generate_feed_items(feed_handler):
                self._save_product(feed, item)
                imported_products += 1
            logger.info("Imported %s products from %s", imported_products, feed)

            imported_feeds += 1
        rs['success_percent'] = 100 * imported_feeds / feeds_count

        return rs

    def _save_product(self, *args, **kwargs):
        try:
            p = self._build_product(*args, **kwargs)
        except ProductBuilderError:
            skip_product = True
            p = None
        else:
            skip_product = False
            if self.filters:
                for f in self.filters:
                    if not f['condition'] or eval(f['condition']):
                        if f['filter'] == 'skip_product':
                            skip_product = True
                        else:
                            self._apply_filter_on_product(p, f)
            if not skip_product:
                if self.storage is not None:
                    self.storage.save_product(p)
                self.saved_products_count += 1
            else:
                self.skipped_products_count += 1
                p = None

        return p
