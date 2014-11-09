from resources.lib.break_api import Client
from resources.lib.kodimon import DirectoryItem

__author__ = 'bromix'


from resources.lib import kodimon

class Provider(kodimon.AbstractProvider):
    def __init__(self):
        kodimon.AbstractProvider.__init__(self)

        self._client = Client()
        pass

    def on_root(self, path, params, re_match):
        result = []

        json_data = self._client.get_home()
        collection = json_data['data']['data']['collection']
        for item in collection:
            title = item['name']
            item_id = str(item['id'])

            if title != u'Galleries':
                root_item = DirectoryItem(title,
                                          self.create_uri(['category', item_id]))
                root_item.set_fanart(self.get_fanart())
                result.append(root_item)
                pass
            pass

        return result
    pass
