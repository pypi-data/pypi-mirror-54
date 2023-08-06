import logging

from productfeeds.importers.base import AbstractImporter
from productfeeds.models import Product

logger = logging.getLogger(__name__)


class DummyImporter(AbstractImporter):
    def __init__(self, feeds=None, articlecode_prefix='dummy_', *args, **kwargs):
        super(DummyImporter, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.feeds = feeds

    def _build_product(self, feed, data):
        p = Product()
        p.d['title'] = data['name']
        p.d['client'] = data['feed_id']
        p.d['price'] = data['price']
        articlecode = self._build_articlecode("{}_{}".format(feed, data['id']))
        p.d['articlecode'] = articlecode
        return p

    def _fetch(self, feed_id):
        data = [
            {'feed_id': feed_id, 'id': '1', 'name': 'Product 1', 'price': 12},
            {'feed_id': feed_id, 'id': '2', 'name': 'Product 2', 'price': 12},
            {'feed_id': feed_id, 'id': '3', 'name': 'Product 3', 'price': 12},
        ]
        return data

    def get_feeds(self):
        return self.feeds

    def _generate_feed_items(self, data):
        for item in data:
            yield item

