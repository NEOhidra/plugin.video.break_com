from resources.lib import kodimon
from resources.lib.break_api import Provider

__author__ = 'bromix'

import unittest


class TestProvider(unittest.TestCase):
    def test_on_root(self):
        provider = Provider()

        result = provider.navigate('/')
        items = result[0]

        kodimon.print_items(items)
        pass
    pass
