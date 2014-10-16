import urllib2
from collections import Iterable


__author__ = "Leandro Voltolino <xupisco@gmail.com>"
__version__ = "0.7"

try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            raise Exception("GiantBomb wrapper requires the simplejson "
                            "library (or Python 2.6) to work. "
                            "http://www.undefined.org/python/")


class GiantBombError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Api:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.giantbomb.com/'

    @staticmethod
    def default_repr(obj):
        return unicode("<%s: %s>" % (obj.id, obj.name)).encode('utf-8')

    def check_response(self, resp):
        if resp['status_code'] == 1:
            return resp['results']
        else:
            raise GiantBombError('Error code %s: %s' % (resp['status_code'],
                                                        resp['error']))

    def _build_url(self, query, params=None):
        url = self.base_url + "%s/?api_key=%s&format=json" % (query,
                                                               self.api_key)
        for key, value in params.iteritems():
            if isinstance(value, dict):
                url += "&%s=" % key
                url += ";".join([subkey+":"+str(subvalue)
                                 for subkey, subvalue in filter.iteritems()])
            else:
                url += "&%s=%s" % (key, str(value))
        return url
        
    def search(self, query, offset=0, resources=None, filter=None, limit=None):
        params = {"offset": offset, 'query': query}
        if resources is not None:
            params['resources'] = resources
        if filter is not None:
            params['filter'] = filter
        if limit is not None:
            params['limit'] = limit
        
        url = self._build_url("search", params=params)

        results = simplejson.load(urllib2.urlopen(url))
        return [SearchResult.NewFromJsonDict(x) for x in self.check_response(results)]

    def get_game(self, id):
        if isinstance(id, int):
            id = id.id
        url = self._build_url('game/%s' % id)
        game = simplejson.load(urllib2.urlopen(url))
        return Game.NewFromJsonDict(self.check_response(game))

    def get_games(self, plat=None, offset=0, filter=None, limit=None):
        params = {"offset": offset}
        if plat is not None:
            if type(plat).__name__ != 'int':
                plat = plat.id
            params['platforms'] = plat
        if filter is not None:
            params['filter'] = filter
        if limit is not None:
            params['limit'] = limit
        
        url = self._build_url("games", params=params)
                       
        games = simplejson.load(urllib2.urlopen(url))
        return [SearchResult.NewFromJsonDict(x)
                for x in self.check_response(games)]

    def get_video(self, id):
        if isinstance(id, int):
            id = id.id
        url = self._build_url('video/%s' % id)
        video = simplejson.load(urllib2.urlopen(url))
        return Video.NewFromJsonDict(self.check_response(video))

    def get_platform(self, id):
        if isinstance(id, int):
            id = id.id
        url = self._build_url('platform/%s' % id)
        platform = simplejson.load(urllib2.urlopen(url))
        return Platform.NewFromJsonDict(self.check_response(platform))

    def get_platforms(self, offset=0, filter=None, limit=None):
        params = {"offset": offset}
        if filter is not None:
            params['filter'] = filter
        if limit is not None:
            params['limit'] = limit
        
        url = self._build_url("platforms", params=params)
                       
        platforms = simplejson.load(urllib2.urlopen(url))
        return self.check_response(platforms)
        
    def get_franchise(self, id):
        if isinstance(id, int):
            id = id.id
        url = self._build_url('franchise/%s' % id)
        franchise = simplejson.load(urllib2.urlopen(url))
        return Franchise.NewFromJsonDict(self.check_response(franchise))
        
    def get_franchises(self, offset=0, limit=None):
        params = {"offset": offset}
        if limit is not None:
            params['limit'] = limit
        
        url = self._build_url("franchises", params=params)
                       
        platforms = simplejson.load(urllib2.urlopen(url))
        return self.check_response(platforms)


class Game:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 platforms=None,
                 developers=None,
                 publishers=None,
                 franchises=None,
                 image=None,
                 images=None,
                 genres=None,
                 original_release_date=None,
                 videos=None,
                 api_detail_url=None,
                 site_detail_url=None,
                 date_added_gb=None,
                 date_last_updated_gb=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.platforms = platforms
        self.developers = developers         
        self.publishers = publishers
        self.franchises = franchises       
        self.image = image
        self.images = images
        self.genres = genres
        self.original_release_date = original_release_date
        self.videos = videos
        self.api_detail_url = api_detail_url
        self.site_detail_url = site_detail_url
        self.date_added_gb = date_added_gb
        self.date_last_updated_gb = date_last_updated_gb

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            franchises_check = data.get('franchises', [])
            platforms_check = data.get('platforms', [])
            images_check = data.get('images', [])
            genres_check = data.get('genres', [])
            videos_check = data.get('videos_check', [])
            list_check = {'franchise': franchises_check, 'platform' : platforms_check, 'image':images_check, 'genre' : genres_check, 'video' : videos_check}
            for item in list_check:
                if not isinstance(list_check[item], Iterable):
                    list_check[item] = None
                           
            return Game(id=data.get('id'),
                        name = data.get('name', None),
                        deck = data.get('deck', None),
                        platforms = list_check['platform'], 
                        developers = data.get('developers', None), 
                        publishers = data.get('publishers', None), 
                        franchises = list_check['franchise'], 
                        image = Image.NewFromJsonDict(data.get('image', [])),
                        images = list_check['image'],
                        genres = list_check['genre'],
                        original_release_date = data.get('original_release_date', None),
                        videos = list_check['video'],
                        api_detail_url = data.get('api_detail_url', None),
                        site_detail_url = data.get('site_detail_url', None),
                        date_added_gb = data.get('date_added', None),  
                        date_last_updated_gb = data.get('date_last_updated', None))        
        return None

    def __repr__(self):
        return Api.default_repr(self)


class Platform:
    def __init__(self,
                 id=None,
                 name=None,
                 abbreviation=None,
                 deck=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.deck = deck
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Platform(id=data.get('id'),
                        name=data.get('name', None),
                        abbreviation=data.get('abbreviation', None),
                        deck=data.get('deck', None),
                        api_detail_url=data.get('api_detail_url', None),
                        image=Image.NewFromJsonDict(data.get('image', None)))
        return None

    def __repr__(self):
        return Api.default_repr(self)
        
class Franchise:
    def __init__(self,
                 id=None,
                 name=None,         
                 deck=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Franchise(id=data.get('id'),
                        name=data.get('name', None),
                        deck=data.get('deck', None),
                        api_detail_url=data.get('api_detail_url', None),
                        image=Image.NewFromJsonDict(data.get('image', None)))
        return None

    def __repr__(self):
        return Api.default_repr(self)
    


class Image:
    def __init__(self,
                 icon=None,
                 medium=None,
                 tiny=None,
                 small=None,
                 thumb=None,
                 screen=None,
                 super=None):

        self.icon = icon
        self.medium = medium
        self.tiny = tiny
        self.small = small
        self.thumb = thumb
        self.screen = screen
        self.super = super

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Image(icon=data.get('icon_url', None),
                         medium=data.get('medium_url', None),
                         tiny=data.get('tiny_url', None),
                         small=data.get('small_url', None),
                         thumb=data.get('thumb_url', None),
                         screen=data.get('screen_url', None),
                         super=data.get('super_url', None),)
        return None

class Genre:
    def __init__(self,
                 id=None,
                 name=None,
                 api_detail_url=None):

        self.id = id
        self.name = name
        self.api_detail_url = api_detail_url

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Genre(id=data.get('id'),
                         name=data.get('name', None),
                         api_detail_url=data.get('api_detail_url', None))
        return None

    def __repr__(self):
        return Api.default_repr(self)


class Videos:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 image=None,
                 url=None,
                 publish_date=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.image = image
        self.url = url
        self.publish_date = publish_date

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Videos(id=data.get('id'),
                         name=data.get('name', None),
                         deck=data.get('deck', None),
                         image=Image.NewFromJsonDict(data.get('image', None)),
                         url=data.get('url', None),
                         publish_date=data.get('publish_date', None),)
        return None

    def __repr__(self):
        return Api.default_repr(self)


class Video:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 image=None,
                 url=None,
                 publish_date=None,
                 site_detail_url=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.image = image
        self.url = url
        self.publish_date = publish_date
        self.site_detail_url = site_detail_url

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Video(id=data.get('id'),
                         name=data.get('name', None),
                         deck=data.get('deck', None),
                         image=Image.NewFromJsonDict(data.get('image', None)),
                         url=data.get('url', None),
                         publish_date=data.get('publish_date', None),
                         site_detail_url=data.get('site_detail_url', None))
        return None

    def __repr__(self):
        return Api.default_repr(self)


class SearchResult:
    def __init__(self,
                 id=None,
                 name=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return SearchResult(id=data.get('id'),
                                name=data.get('name', None),
                                api_detail_url=data.get('api_detail_url', None),
                                image=data.get('image', None))
        return None

    def __repr__(self):
        return Api.default_repr(self)
