from resources.lib.break_api import Client
from resources.lib.kodimon import DirectoryItem, VideoItem
from resources.lib.kodimon.helper import FunctionCache

__author__ = 'bromix'


from resources.lib import kodimon

class Provider(kodimon.AbstractProvider):
    def __init__(self):
        kodimon.AbstractProvider.__init__(self)

        self._client = Client()
        pass

    def _feed_to_item(self, json_data):
        result = []

        data = json_data['data']['data']
        for item in data:
            video_item = VideoItem(item['title'],
                                   self.create_uri(['play']))
            video_item.set_fanart(self.get_fanart())
            video_item.set_plot(item['description'])
            image = item.get('thumbnails', [])
            if len(image) > 0:
                image = image[0].get('url', '')
                video_item.set_image(image)
                pass
            result.append(video_item)
            pass

        return result

    @kodimon.RegisterPath('^/feed/(?P<feed_id>.*)/$')
    def _on_feed(self, path, params, re_match):
        self.set_content_type(kodimon.constants.CONTENT_TYPE_EPISODES)
        result = []

        feed_id = int(re_match.group('feed_id'))
        page = int(params.get('page', 1))

        json_data = self.get_function_cache().get(FunctionCache.ONE_MINUTE, self._client.get_feed, feed_id, page)
        result.extend(self._feed_to_item(json_data))

        # test next page
        next_page = page+1
        json_data = self.get_function_cache().get(FunctionCache.ONE_MINUTE, self._client.get_feed, feed_id, next_page)
        next_page_result = self._feed_to_item(json_data)
        if len(next_page_result) > 0:
            next_page_item = self.create_next_page_item(page, path, params)
            result.append(next_page_item)
            pass

        return result

    def on_root(self, path, params, re_match):
        result = []

        json_data = self._client.get_home()
        collection = json_data['data']['data']['collection']
        for item in collection:
            title = item['name']
            if title != u'Galleries':
                item_id = str(item['id'])
                feed_item = DirectoryItem(title,
                                          self.create_uri(['feed', item_id]))
                feed_item.set_fanart(self.get_fanart())
                result.append(feed_item)
                pass
            pass

        return result
    pass
