from resources.lib.break_api import Client

__author__ = 'bromix'

import unittest


class TestClient(unittest.TestCase):
    def test_get_feed(self):
        client = Client()
        json_data = client.get_feed(40)
        pass

    def test_get_home(self):
        client = Client()
        json_data = client.get_home()
        pass
    pass
