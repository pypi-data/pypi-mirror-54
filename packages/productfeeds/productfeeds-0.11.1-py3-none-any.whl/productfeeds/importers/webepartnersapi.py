# -*- coding: utf-8 -*-
# Forked original script written by Daniel Pawelec
import sys

import requests
import logging
import json
import time
import re
import xml.etree.ElementTree as ET
import unicodedata
import random

from .base import AbstractImporter, ProductBuilderError
from productfeeds.models import Product

logger = logging.getLogger(__name__)

PRODUCT_URL_TEMPLATE = 'http://api.webepartners.pl/wydawca/XML?programid={program_id}&page=1&pageSize={page_size}'
PROGRAMS_URL = 'http://api.webepartners.pl/wydawca/Programs'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 '
                  'Safari/537.36'}


class WebepartnersImporter(AbstractImporter):

    def __init__(self, login=None, password=None, programs=None, articlecode_prefix='web_', page_size=20000, *args, **kwargs):
        super(WebepartnersImporter, self).__init__(*args, articlecode_prefix=articlecode_prefix, **kwargs)
        self.page_size = page_size
        self.login = login
        self.password = password
        self.programs = {}
        self.articlecodes_set = set()
        if programs is not None:
            self.programs = {p['name']: p['categories'] for p in programs if p}

    def get_feeds(self):
        # get list of programs
        response = requests.get(PROGRAMS_URL, auth=(self.login, self.password), headers=HEADERS)

        if response.status_code != 200:
            logger.debug("REST API connection error: %s \n" % response.status_code)

        data = response.content

        data = json.loads(data)

        programs = []

        for row in data:
            # normalize

            if self.programs is None or row['ProgramName'] in self.programs:
                programs.append({'program_id': row['ProgramId'], 'program_name': row['ProgramName']})

        return programs

    def _fetch(self, program):
        url = PRODUCT_URL_TEMPLATE.format(program_id=program['program_id'], page_size=self.page_size)
        response = requests.get(url, auth=(self.login, self.password), headers=HEADERS)
        return response.content

    def _generate_feed_items(self, xml_content):
                # parse XML
        if sys.version_info[0] >= 3:
            xml_content = xml_content.decode('utf-8')
        xml_content = xml_content.replace('\\"', '"').replace('\\n', '')
        xml_content = xml_content.strip('"')
        try:
            products = ET.fromstring(xml_content)
        except Exception as e:
            print(e)
            logger.info("\tno products found")
            raise Exception('No products found')

        logger.debug("\tfound products:%s" % len(products))

        if len(products) > 0:
            logger.debug("\tImporting ...")

        failures = 0
        for product in products:
            yield product

    def _build_product(self, program, product):
        p = Product()
        p.d['client'] = program['program_name']

        # articlecode
        p.d['articlecode'] = '%s%s_%s' % (
            self.prefix, product.find('awId').text.strip(), product.find('pId').text.strip())

        if p.d['articlecode'] in self.articlecodes_set:
            raise ProductBuilderError('{} already imported'.format(p.d['articlecode']))
        # title
        if not product.find('name').text:
            raise ProductBuilderError('Product name in {} is empty'.format(p.d['articlecode']))

        name = product.find('name').text

        name = re.sub(r'"?__.*', '', name)
        name = name.strip()
        if type(name).__name__ == 'unicode':
            name = name.encode('utf-8')
        p.d['title'] = name


        # categories
        try:
            fullcat = product.find('awCat').text
            categories = fullcat.split('/')
            p.d['category'] = categories[0]
            p.d['subcategory1'] = categories[1]
        except AttributeError:

            p.d['category'] = program['program_name']
        else:
            try:
                p.d['subcategory2'] = categories[2]
            except IndexError:
                pass

        # brand
        try:
            p.d['brand'] = product.find('brand').text
        except AttributeError:
            pass

        try:
            p.d['description'] = product.find('desc').text
        except AttributeError:
            pass

        # productUrl
        p.d['producturl'] = product.find('awLink').text

        # thumbUrl
        try:
            p.d['thumburl'] = product.find('awThumb').text
        except AttributeError:
            pass

        # imageUrl
        p.d['imageurl'] = product.find('awImage').text

        # deliveryTime
        try:
            p.d['delivery'] = product.find('deliveryTime').text
        except AttributeError:
            pass
        if sys.version_info[0] < 3:
            p.d['category'] = p.d['category'].encode('utf-8')
        # price
        p.d['price'] = product.find('price').text
        # print type(p.product_data['price'])
        if float(p.d['price']) == 0:
            raise ProductBuilderError('Price in {} is 0'.format(p.d['articlecode']))

        # remove whitespaces
        for key in p.d:
            try:
                p.d[key] = p.d[key].strip()
            except:
                pass
        if not (not self.programs[program['program_name']] or p.d['category'] in self.programs[program['program_name']]):
            raise ProductBuilderError('Category & program name rule broken in {}'.format(p.d['articlecode']))
        self.articlecodes_set.add(p.d['articlecode'])
        return p

