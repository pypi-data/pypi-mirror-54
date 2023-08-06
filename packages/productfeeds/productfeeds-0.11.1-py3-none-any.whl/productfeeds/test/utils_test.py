import unittest
from os.path import dirname, join

from productfeeds.utils import load_custom_library


class TestUtils(unittest.TestCase):
    def test_load_custom_library_ok(self):
        a = load_custom_library('datetime:datetime')
        self.assertEqual(a.__name__, 'datetime')

    def test_load_custom_library_failure(self):
        with self.assertRaises(AttributeError):
            a = load_custom_library('datetime:datetimee')

