# -*- coding: utf-8 -*-

import os
import urllib2
import urlparse
 
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

#import pydevd
#pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)

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
        
        # first try to get the normal video urls
        test = xml.find('ContentURL')
        if test!=None:
            result = test.text
        test = xml.find('VideoSource')
        if test!=None:
            result = test.text
            
        vq = __plugin__.getSettingAsInt('videoQuality', 1)
        vh = 720
        if vq==1:
            vh=720
        elif vq==0:
            vh=480
        else:
            vh = 720

        # try the media-group
        try:
            mediaGroup = xml.find('media-group')
            if mediaGroup!=None:
                oldHeight = 0
                for mediaContent in mediaGroup:
                    testHeight = int(mediaContent.get('height'))
                    if testHeight>=oldHeight and testHeight<=vh:
                        result = mediaContent.get('url')
                        oldHeight = testHeight
                    pass 
                pass
        except:
            # do nothing
            pass
            
        # try for direct tags
        videoUrlList = ['Video%sURL' % (str(vh)), 'Video720URL', 'Video480URL']
        for videoUrl in videoUrlList:
            test = xml.find(videoUrl)
            if test!=None:
                result = test.text
                break
            
        # first tests for youtube url
        if result and result.find('?')>0:
            pos = result.find('?')
            pos+=1
            args = urlparse.parse_qs(result[pos:])
            value = args.get('v', None)
            if value and len(value)>=1:
                result = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s" % (value[0])
                
        # second tests for youtube url
        test = xml.find('ContentEmbedSourceName')
        if test!=None and test.text=='YouTube':
            test = xml.find('ThirdPartyUniqueId')
            if test!=None:
                result = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s" % (test.text)

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