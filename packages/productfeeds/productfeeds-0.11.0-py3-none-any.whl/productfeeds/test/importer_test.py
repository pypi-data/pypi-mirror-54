import unittest

import requests_mock

from productfeeds.importers.convertiserapi import ConvertiserImporter
from productfeeds.importers.webepartnersapi import WebepartnersImporter
from productfeeds.base import build_importer, build_storage
from productfeeds.models import Product, ProductError
from productfeeds.storage.dummystorage import DummyStorage


class DummyTestStorage(object):
    def __init__(self, settings=None):
        self.products = []
        self.article_codes = set()

    def save_product(self, p):
        self.products.append(p.to_dict())
        self.article_codes.add(p.get('articlecode'))


class TestImporter(unittest.TestCase):

    def test_build_importer(self):
        importer = build_importer('webepartners', {})
        self.assertIsInstance(importer, WebepartnersImporter)
        importer = build_importer('convertiser', {})
        self.assertIsInstance(importer, ConvertiserImporter)
        with self.assertRaises(Exception) as ex:
            build_importer('undefined-API', {})

    def test_build_storage(self):
        storage = build_storage('dummy', {})
        self.assertIsInstance(storage, DummyStorage)
        with self.assertRaises(KeyError):
            storage = build_storage('dummyyyy', {})

    def test_product_model(self):
        a = 'my_article_code'
        p = Product()
        p.set('articlecode', a)
        self.assertEquals(p.get('articlecode'), a)
        self.assertEquals(p.d['articlecode'], a)
        with self.assertRaises(ProductError):
            Product({'dict': 'without required field'})

    def test_filters_ok(self):
        """
        Filters applying test
        """
        settings = {'token': '123', 'offers': [123], 'website_key': '321', 'articlecode_prefix': 'p_'}
        api = ConvertiserImporter(storage=None, **settings)
        api.filters = [
            {'condition': "not p.d['category']", 'field': 'category', 'filter': 'copy:$title'},
            {'condition': None, 'field': 'title', 'filter': 'capitalize:$title'},
            {'condition': "p.d['brand'] is None", 'field': 'brand', 'filter': 'capitalize:$brand'},
            {'condition': "p.d['brand'] is not None", 'field': 'client', 'filter': 'capitalize:$brand'},
            {'condition': None, 'field': 'imageurl', 'filter': 'urlencode:$imageurl'},
            {'condition': None, 'field': 'imageurl', 'filter': 'join:prefix://wp.pl?url=:$imageurl'},
            {'condition': None, 'field': 'producturl', 'filter': ['join', 'http://hurra.com?url=', '$producturl']},

        ]
        p_d = {
            'id': 111,
            'title': 'vEry uGLY',
            'brand': 'DONT CHANGE',
            'description': '',
            'link': 'http://wp.pl',
            'images': {'thumb_180': '', 'default': 'http://localhost.pl/image.jpg'},
            'price': '123,12',
            'offer_id': '123',
            'offer': 'SHOULD BE CHANGED',
            'product_type': ''
        }
        p = api._save_product('my_feed', p_d)
        self.assertEqual(p.d['category'], 'vEry uGLY')
        self.assertEqual(p.d['title'], 'Very Ugly')
        self.assertEqual(p.d['brand'], 'DONT CHANGE')
        self.assertEqual(p.d['client'], 'Dont Change')
        self.assertEqual(p.d['imageurl'], 'prefix//wp.pl?url=http%3A%2F%2Flocalhost.pl%2Fimage.jpg')
        self.assertEqual(p.d['producturl'], 'http://hurra.com?url=http://wp.pl')

    def test_filter_skip(self):
        settings = {'token': '123', 'offers': [123], 'website_key': '321', 'articlecode_prefix': 'p_'}
        api = ConvertiserImporter(storage=None, **settings)
        api.filters = [
            {'condition': "p.d['brand'] == 'DONT CHANGE'", 'filter': 'skip_product'},
        ]
        p_d = {
            'id': 111,
            'title': 'vEry uGLY',
            'brand': 'DONT CHANGE',
            'description': '',
            'link': '',
            'images': {'thumb_180': '', 'default': ''},
            'price': '123,12',
            'offer_id': '123',
            'offer': 'SHOULD BE CHANGED',
            'product_type': ''
        }
        p = api._save_product('my_feed', p_d)
        self.assertTrue(p is None)
        api.filters = [
            {'condition': "p.d['brand'] == 'DONT CHANGE'", 'filter': 'skip_product'},
        ]
        p_d['brand'] = 'New brand'

        p = api._save_product('my_feed', p_d)
        self.assertTrue(isinstance(p, Product))

    def test_convertiser(self):
        storage = DummyTestStorage()
        settings = {'token': '123', 'offers': [123], 'website_key': '321', 'articlecode_prefix': 'p_'}
        api = ConvertiserImporter(storage=storage, **settings)
        with requests_mock.mock() as m:
            url = 'https://api.convertiser.com/publisher/products/v2/?key={}'.format(settings['website_key'])
            m.post(
                url,
                text='{"count":100000,"pagination":{"previous_page":null,"page":0,"page_size":50,"next_page":1},'
                     '"data":[{"id":"123123123",'
                     '"title":"GOODRAM USB 2.0 32GB 20MB/s UMO2-0320O0R11","description":"Specyfikacja: Parametry '
                     'ogolne - Kolor: Pomaranczowy, Wymiary mm: 54 x 18 x 8,5 mm, Waga g: 7,5 g, Parametry '
                     'techniczne","price":"PLN 19.22","sale_price":null,"sale_price_effective_date":"",'
                     '"discount":0,"offer":"Offerer","offer_id":"999","brand":"GOODRAM","images":'
                     '{"thumb_43":"https://img.convertiser.com/cnGdhDIrNF_","default":"https://img.convertiser.com/hg"'
                     ',"thumb_180":"https://img.convertiser.com/bzfg-HKx5E1KBOWcdi1C"},'
                     '"image_link":"https://static.convertiser.com/media/product_images/23","additional_images":{},'
                     '"additional_image_link":null,"link":"https://converti.se/click/0569ea91-71526c8b-f4.html",'
                     '"mobile_link":"https://converti.se/click/0569ea91-71.html","direct_link":"https://www.sfdsd.pl",'
                     '"google_product_category":"Komputery/Przechowywanie danych/PenDrive","product_type":"Komputery",'
                     '"gtin":"","mpn":"","color":"","gender":"","age_group":"","material":"","pattern":"","size":"",'
                     '"size_system":"","item_group_id":"","multipack":null,"is_bundle":null,"adult":null,'
                     '"updated_at":"2019-02-09T05:15:26.154018+00:00","offer_display_url":"http://www.sdfsdf.pl/",'
                     '"is_cpc":false,"cpc_rate":"PLN 0.00"}]}'
            )
            rs = api.import_products()
        self.assertEquals({'status': 1, 'success_percent': 100}, rs)
        self.assertTrue('p_999_123123123' in storage.article_codes)
