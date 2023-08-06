import sys
import time
import requests
import logging
import json

from retrypy import retry

from .base import AbstractImporter
from productfeeds.models import Product

logger = logging.getLogger(__name__)

PRODUCTS_URL = 'https://api.convertiser.com/publisher/products/v2/?key={}'
REQUEST_TIMEOUT = 120
SLEEP_BETWEEN_REQUESTS = 15


class ConvertiserImporterException(Exception):
    pass


class ConvertiserImporter(AbstractImporter):

    def __init__(self, token=None, offers=None, website_key=None, articlecode_prefix='con_', page_size=20000,
                 *args, **kwargs):

        super(ConvertiserImporter, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.page_size = page_size
        self.website_key = website_key
        self.offers = offers
        self.token = token

    def get_feeds(self):
        return self.offers

    @retry.decorate(Exception, times=3, wait=SLEEP_BETWEEN_REQUESTS)
    def _fetch_products(self, current_page, offer):
        response = requests.post(
                        PRODUCTS_URL.format(self.website_key),
                        headers={'Authorization': 'Token {}'.format(self.token), 'Content-Type': 'application/json'},
                        data=json.dumps({
                            "filters": {"offer_id": {"lookup": "exact", "value": offer}},
                            "page": current_page, "page_size": self.page_size
                        }),
                        timeout=REQUEST_TIMEOUT
                 )

        if response.status_code != 200:
            logger.warning("Status code is {}".format(response.status_code))
            raise ConvertiserImporterException('Status code is not 200')
        try:
            rs = response.json()
        except Exception:
            logger.warning('Improperly formatted JSON response')
            raise ConvertiserImporterException('Improperly formatted JSON response')

        return rs

    def _fetch(self, feed):
        if not isinstance(feed, dict):
            feed_obj = {'feed_id': feed}
        else:
            feed_obj = feed
        offer = feed_obj['feed_id']

        all_products = {'data': []}
        current_products_count = None
        current_page = 1
        while current_products_count is None or current_products_count == self.page_size:
            logger.info("Read page {}".format(current_page))

            rs = self._fetch_products(current_page, offer)

            current_products_count = len(rs['data'])
            logger.info("Read {} products".format(current_products_count))
            all_products['data'] += rs['data']
            current_page += 1
            logger.info("Total imported products {}, sleep 15 seconds".format(len(all_products['data'])))
            if current_products_count == self.page_size:
                time.sleep(SLEEP_BETWEEN_REQUESTS)

        self.unique_values = []
        return all_products

    def _generate_feed_items(self, data):
        for item in data['data']:
            yield item

    def _build_product(self, feed, product):
        if not isinstance(feed, dict):
            feed_obj = {'feed_id': feed}
        else:
            feed_obj = feed
        p = Product()
        p.d['client'] = product['offer']
        articlecode = self._build_articlecode("{}_{}".format(product['offer_id'], product['id']))
        p.d['articlecode'] = articlecode
        p.d['title'] = product['title']
        p.d['brand'] = product['brand']
        categories = product['product_type'].split('/')
        p.d['category'] = categories[0]
        try:
            p.d['subcategory1'] = categories[1]
        except:
            pass
        try:
            p.d['subcategory2'] = categories[2]
        except:
            pass
        p.d['description'] = product['description']
        if sys.version_info[0] < 3:
            p.d['title'] = p.d['title'].encode('utf-8')
            p.d['description'] = p.d['description'].encode('utf-8')
            p.d['brand'] = p.d['brand'].encode('utf-8')
            p.d['category'] = p.d['category'].encode('utf-8')
        p.d['producturl'] = product['link']
        p.d['thumburl'] = product['images']['thumb_180']
        p.d['imageurl'] = product['images']['default']
        p.d['price'] = product['price'].replace('PLN ', '')
        if 'unique_key' in feed_obj:
            if product[feed_obj['unique_key']] in self.unique_values:
                p.d['non_unique'] = True
            else:
                self.unique_values.append(product[feed_obj['unique_key']])

        return p
