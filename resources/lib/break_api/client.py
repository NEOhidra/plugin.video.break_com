import json
import requests

__author__ = 'bromix'


class Client(object):
    def __init__(self):
        self._page_size = 25
        pass

    def get_video_url(self, video_id, max_video_quality=720):
        json_data = self.get_video(video_id)
        data = json_data['data']
        hls_uri = data['hlsUri']
        if hls_uri:
            token = data['token']

            bit_rates = []
            media_files = data['mediaFiles']
            for media_file in media_files:
                # someone switched the values
                height = int(media_file['width'])
                bit_rate = str(media_file['bitRate'])
                if len(bit_rate) <= 4 and height <= max_video_quality:
                    bit_rates.append(bit_rate)
                    pass
                pass
            bit_rates = ','.join(bit_rates)

            url = '%s,%s,_kbps.mp4.m3u8?%s' % (hls_uri, bit_rates, token)
            return url

        # try youtube
        youtube_video_id = data['thirdPartyUniqueId']
        return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + youtube_video_id

    def get_video(self, video_id):
        headers = {'Content-Type': 'application/json'}
        post_data = json.dumps({'id': int(video_id)})
        return self._perform_request(method='POST', path='/content/video/get', post_data=post_data, headers=headers)

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
                    'Connection': 'Keep-Alive',
                    'User-Agent': ''}
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