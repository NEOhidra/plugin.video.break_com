# -*- coding: utf-8 -*-

import os
import urllib2
try:
    from xml.etree import ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import bromixbmc

__channel__ = [{'title': 'Featured Videos',
                'id': '-1'
                },
               {'title': 'Pranks & Fails',
                'id': '534'
                },
               {'title': 'Trailers',
                'id': '531'
                },
               {'title': 'Sports',
                'id': '533'
                },
               {'title': 'Bizarre & Amazing',
                'id': '537'
                },
               {'title': 'Heartwarming',
                'id': '536'
                },
               {'title': 'All the animals',
                'id': '535'
                },
               ]

import pydevd
pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)

__plugin__ = bromixbmc.Plugin()

__FANART__ = os.path.join(__plugin__.getPath(), "fanart.jpg")
if not __plugin__.getSettingAsBool('showFanart'):
    __FANART__ = ''
__ICON__ = os.path.join(__plugin__.getPath(), "icon.png")
__ICON_HIGHLIGHTS__ = os.path.join(__plugin__.getPath(), "resources/media/highlight.png")
__ICON_SEARCH__ = os.path.join(__plugin__.getPath(), "resources/media/search.png")

__ACTION_SHOW_CHANNEL__ = 'showChannel'
__ACTION_PLAY__ = 'play'
__ACTION_SEARCH__ = 'search'

def _getChannelContentXml(id, page):
    result = None
    
    url = 'http://api.break.com'
    if id=='-1':
        url+='/invoke/homepage/includeyoutube/'
    else:
        url+='/invoke/channel/includeyoutube/'
        url+=id
        url+='/'
        
    url+=str(page)+'/'
    url+='25/'
    
    if id!='-1':
        url+='PG/'
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'stagefright/1.2 (Linux;Android 4.4.2)')
                         ]
    try:
        content = opener.open(url)
        result = ET.XML(content.read())
    except:
        # do nothing
        pass
    
    return result

def showIndex():
    for channel in __channel__:
        params = {'action': __ACTION_SHOW_CHANNEL__,
                  'id': channel['id']}
        __plugin__.addDirectory(channel['title'], params=params, thumbnailImage=__ICON__, fanart=__FANART__)
        pass
    
    params = {'action': __ACTION_SEARCH__}
    __plugin__.addDirectory("[B]"+__plugin__.localize(30000)+"[/B]", params = params, thumbnailImage=__ICON_SEARCH__, fanart=__FANART__)
    
    __plugin__.endOfDirectory()
    
def search():
    success = False
    
    keyboard = bromixbmc.Keyboard(__plugin__.localize(30000))
    if keyboard.doModal():
        success = True
        
        search_string = keyboard.getText().replace(" ", "+")
        #result = _request('/capi-2.0a/search', params = {'q': search_string})
        #posts = result.get('posts', [])
        #_listPosts(posts)
        
    __plugin__.endOfDirectory(success)
    
def showChannel(id, page):
    def _getBestVideoUrl(xml):
        result = None
        test = xml.find('ContentURL')
        if test!=None:
            result = test.text
        
        test = xml.find('VideoSource')
        if test!=None:
            result = test.text

        return result
    
    xml = _getChannelContentXml(id, page)
    if xml:
        pageCount = 0
        try:
            pageCount = int(xml.get('PageCount'))
        except:
            pageCount = 1
            
        for content in xml:
            contentName = content.find('ContentTitle').text
            contentId = content.find('ContentID').text
            contentPlot = content.find('ContentDescription').text
            contentThumb = content.find('ThumbNailURL').text
                 
            if contentId and contentName:
                videoUrl = _getBestVideoUrl(content)
                
                params = {'action': __ACTION_PLAY__,
                          'id': contentId,
                          'url': videoUrl
                          }
                infoLabels = {'plot': contentPlot}
                
                __plugin__.addVideoLink(name=contentName, params=params, infoLabels=infoLabels, thumbnailImage=contentThumb, fanart=__FANART__)
        
        if page<pageCount:
            params = {'action': __ACTION_SHOW_CHANNEL__,
                      'id': id,
                      'page': str(page+1)
                      }
            __plugin__.addDirectory(__plugin__.localize(30001)+' ('+str(page+1)+')', params=params, fanart=__FANART__)
    
    __plugin__.endOfDirectory()
    
def play(url):
    __plugin__.setResolvedUrl(url)


action = bromixbmc.getParam('action')
id = bromixbmc.getParam('id')
page = int(bromixbmc.getParam('page', '1'))
url = bromixbmc.getParam('url')

if action == __ACTION_SHOW_CHANNEL__ and id:
    showChannel(id, page)
elif action == __ACTION_PLAY__ and url:
    play(url)
elif action == __ACTION_SEARCH__:
    search()
else:
    showIndex()