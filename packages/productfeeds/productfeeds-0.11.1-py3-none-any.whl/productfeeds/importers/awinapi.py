import csv
import gzip
import logging
import os

import requests

from productfeeds.importers.base import AbstractImporter, ProductBuilderError
from productfeeds.models import Product

DEFAULT_ATTRIBUTES = "aw_deep_link,product_name,aw_product_id,merchant_product_id,merchant_image_url,description,merchant_category,search_price,store_price,aw_image_url,merchant_name,merchant_id,category_name,category_id,currency,delivery_cost,merchant_deep_link,language,last_updated,display_price,data_feed_id,brand_name,merchant_thumb_url,large_image,alternate_image,aw_thumb_url,alternate_image_two,alternate_image_three,alternate_image_four,merchant_product_category_path"
URL_PATTERN = "https://productdata.awin.com/datafeed/download/apikey/{api_key}/language/{language_code}/fid/{feed_id}" \
              "/columns/{attributes}/format/csv/delimiter/%3B/excel/1/compression/gzip/adultcontent/1/"

logger = logging.getLogger(__name__)


class AwinImporter(AbstractImporter):
    def __init__(self, api_key=None, feeds=None, language_code="pl", articlecode_prefix='awin_', *args, **kwargs):
        super(AwinImporter, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.api_key = api_key
        self.language_code = language_code
        self.prefix = articlecode_prefix
        self.feeds = feeds

    def get_feeds(self):
        return self.feeds

    def _fetch(self, feed):
        if not isinstance(feed, dict):
            feed_obj = {'feed_id': feed}
        else:
            feed_obj = feed

        url = URL_PATTERN.format(
            api_key=self.api_key, language_code=self.language_code, feed_id=feed_obj['feed_id'], attributes=DEFAULT_ATTRIBUTES,
        )
        r = requests.get(url, allow_redirects=True)
        compressed_feed_file_path = os.path.join(self.tmp_dir, 'awin-feed.csv.gz')
        decompressed_feedfile_path = compressed_feed_file_path[:-3]
        with open(compressed_feed_file_path, 'wb') as f:
            f.write(r.content)
        with open(decompressed_feedfile_path, "wb") as fw:
            with gzip.open(compressed_feed_file_path, 'rb') as f:
                f.read(3)  # header
                fw.write(f.read())
        os.unlink(compressed_feed_file_path)
        self.unique_values = []
        return decompressed_feedfile_path

    def _build_product(self, feed, item):
        if not isinstance(feed, dict):
            feed_obj = {'feed_id': feed}
        else:
            feed_obj = feed

        row = item[0]
        columns_map = item[1]

        product = {columns_map[map_index]: column for map_index, column in enumerate(row)}
        p = Product()
        articlecode = self._build_articlecode("{}_{}".format(feed_obj['feed_id'], product['merchant_product_id']))
        p.d['articlecode'] = articlecode
        p.d['client'] = product['merchant_name']
        p.d['title'] = product['product_name']
        p.d['brand'] = product['brand_name']
        if 'unique_key' in feed_obj:

            if product[feed_obj['unique_key']] in self.unique_values:
                p.d['non_unique'] = True
            else:
                self.unique_values.append(product[feed_obj['unique_key']])

        categories = product['merchant_product_category_path']
        if not categories:
            categories = product['merchant_category']

        if categories:
            categories_list = categories.split(' > ')
            if categories_list:
                try:
                    p.d['category'] = categories_list[0]
                except IndexError:
                    pass
                try:
                    p.d['subcategory1'] = categories_list[1]
                except IndexError:
                    pass
                try:
                    p.d['subcategory2'] = categories_list[2]
                except IndexError:
                    pass

        #p.d['category'] = product['merchant_category']
        if not p.d['category']:
            p.d['category'] = p.d['client']

        p.d['description'] = product['description']
        p.d['producturl'] = product['aw_deep_link']
        p.d['thumburl'] = product['aw_image_url']
        p.d['imageurl'] = product['merchant_image_url']
        if not p.d['imageurl']:
            p.d['imageurl'] = p.d['thumburl']
        p.d['price'] = product['display_price'].replace('PLN', '')

        if float(p.d['price']) == 0:
            raise ProductBuilderError('Price in {} is 0'.format(p.d['articlecode']))

        return p

    def _generate_feed_items(self, handler):
        with open(handler, 'r') as csvfile:
            csv_rows = csv.reader(csvfile, delimiter=';', quotechar='"')
            columns_map = {}
            first_row = next(csv_rows)

            for i, column in enumerate(first_row):
                columns_map[i] = column

            for row in csv_rows:
                yield row, columns_map

        os.unlink(handler)

