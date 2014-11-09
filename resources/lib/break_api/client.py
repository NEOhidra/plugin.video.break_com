import json
import requests

__author__ = 'bromix'


class Client(object):
    def __init__(self):
        self._page_size = 25
        pass

    def get_feed(self, feed_id, page=1):
        api_request_json = {
            'requestedProperties': ["title", "description", "contentType", "contentSubType", "thumbnails", "viewCount",
                                    "mediaFiles", "contentPartnerName", "prerollAllowed"],
            'id': feed_id,'pageSize': self._page_size, 'pageNumber': page}
        params = {'apiRequestJson': json.dumps(api_request_json)}
        return self._perform_request(path='/content/contentfeed/get', params=params)

    def get_home(self):
        api_request_json = {'id': 12}
        params = {'apiRequestJson': json.dumps(api_request_json)}
        return self._perform_request(path='/content/FeedQuery/GetFeedCollection', params=params)

    def _perform_request(self, method='GET', headers=None, path=None, post_data=None, params=None,
                         allow_redirects=True):
        # params
        if not params:
            params = {}
            pass
        _params = {}
        _params.update(params)

        # headers
        if not headers:
            headers = {}
            pass

        _headers = {'Host': 'api.breakmedia.com',
                    'Connection': 'Keep-Alive'}
        _headers.update(headers)

        # url
        _url = 'http://api.breakmedia.com/%s' % path.strip('/')

        result = None
        if method == 'GET':
            result = requests.get(_url, params=_params, headers=_headers, verify=False, allow_redirects=allow_redirects)
        elif method == 'POST':
            result = requests.post(_url, data=post_data, params=_params, headers=_headers, verify=False,
                                   allow_redirects=allow_redirects)

        if result is None:
            return {}

        return result.json()

    pass