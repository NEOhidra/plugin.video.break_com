# -*- coding: utf-8 -*-

import os

import bromixbmc

__channel__ = [{'title': 'Featured Videos',
                'id': ''
                },
               {'title': 'Pranks & Fails',
                'id': ''
                },
               {'title': 'Trailers',
                'id': ''
                },
               {'title': 'Sports',
                'id': ''
                },
               {'title': 'Bizarre & Amazing',
                'id': ''
                },
               {'title': 'Heartwarming',
                'id': ''
                },
               {'title': 'All the animals',
                'id': ''
                },
               ]

#import pydevd
#pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)

__plugin__ = bromixbmc.Plugin()

__FANART__ = os.path.join(__plugin__.getPath(), "fanart.jpg")
__ICON_HIGHLIGHTS__ = os.path.join(__plugin__.getPath(), "resources/media/highlight.png")
__ICON_SEARCH__ = os.path.join(__plugin__.getPath(), "resources/media/search.png")

__ACTION_SEARCH__ = 'search'

def showIndex():
    for channel in __channel__:
        __plugin__.addDirectory(channel['title'], fanart=__FANART__)
        pass
    
    params = {'action': __ACTION_SEARCH__}
    __plugin__.addDirectory("[B]"+__plugin__.localize(30000)+"[/B]", params = params, thumbnailImage=__ICON_SEARCH__, fanart=__FANART__)
    
    __plugin__.endOfDirectory()


showIndex()