'''
GiantBomb is an interface to the API on giantbomb.com.
'''

__author__ = "Leandro Voltolino <xupisco@gmail.com>"
__version__ = "0.7"

import urllib2
import urllib
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
    '''Generic exception class'''

    pass


def check_response(resp):
    '''
    Performs a quick verification of the response to ensure we have
    valid data
    '''

    if resp['status_code'] == 1:
        return resp['results']
    else:
        raise GiantBombError('Error code %s: %s' % (resp['status_code'],
                                                    resp['error']))


class Api:
    '''
    The primary interface for the GiantBomb module.  Instantiate this with
    your api key and then call the appropriate methods to access the data
    from the giantbomb servers.
    '''

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.giantbomb.com/'

    @staticmethod
    def default_repr(obj):
        '''provide a basic representation of this object'''

        return unicode("<%s: %s>" % (obj.id, obj.name)).encode('utf-8')

    def _build_url(self, query, params=None):
        '''Helper to build the URL from a parameter dictionary'''

        url = self.base_url + "%s/?api_key=%s&format=json" % (query,
                                                              self.api_key)
        if params:
            for key, value in params.iteritems():
                if isinstance(value, dict):
                    vals = [subkey + ":" + str(subvalue)
                            for subkey, subvalue in value.iteritems()]
                    url += "&%s=" % key
                    url += ";".join(vals)
                else:
                    url += "&%s=%s" % (key, str(value))
        return url

    def get_franchise(self, gbid):
        '''
        Get the franchise:
        http://www.giantbomb.com/api/documentation#toc-0-12
        '''

        if not isinstance(gbid, int):
            gbid = gbid.id
        url = self._build_url('franchise/%s' % gbid)
        franchise = simplejson.load(urllib2.urlopen(url))
        return Franchise(check_response(franchise))

    def get_franchises(self, offset=0, limit=None):
        '''
        Get the franchises:
        http://www.giantbomb.com/api/documentation#toc-0-13
        '''

        params = {"offset": offset}
        if limit is not None:
            params['limit'] = limit

        url = self._build_url("franchises", params=params)

        franchise = simplejson.load(urllib2.urlopen(url))
        return [Franchise(x)
                for x in check_response(franchise)]

    def get_game(self, gbid):
        '''
        Get the game
        http://www.giantbomb.com/api/documentation#toc-0-14
        '''

        if not isinstance(gbid, int):
            gbid = gbid.id
        url = self._build_url('game/%s' % gbid)
        game = simplejson.load(urllib2.urlopen(url))
        return Game(check_response(game))

    def get_games(self, plat=None, offset=0, gbfilter=None, limit=None):
        '''
        Get the games
        http://www.giantbomb.com/api/documentation#toc-0-15
        '''

        params = {"offset": offset}
        if plat is not None:
            if type(plat).__name__ != 'int':
                plat = plat.id
            params['platforms'] = plat
        if gbfilter is not None:
            params['filter'] = gbfilter
        if limit is not None:
            params['limit'] = limit

        url = self._build_url("games", params=params)

        games = simplejson.load(urllib2.urlopen(url))
        return [SearchResult(x)
                for x in check_response(games)]

    def get_platform(self, gbid):
        '''
        Get the platform
        http://www.giantbomb.com/api/documentation#toc-0-26
        '''

        if not isinstance(gbid, int):
            gbid = gbid.id
        url = self._build_url('platform/%s' % gbid)
        platform = simplejson.load(urllib2.urlopen(url))
        return Platform(check_response(platform))

    def get_platforms(self, offset=0, gbfilter=None, limit=None):
        '''
        Get the platforms
        http://www.giantbomb.com/api/documentation#toc-0-27
        '''

        params = {"offset": offset}
        if gbfilter is not None:
            params['filter'] = gbfilter
        if limit is not None:
            params['limit'] = limit

        url = self._build_url("platforms", params=params)

        platforms = simplejson.load(urllib2.urlopen(url))
        return [Platform(x)
                for x in check_response(platforms)]

    def search(self, query, offset=0, resources=None, gbfilter=None,
               limit=None):
        '''
        Perform a search
        http://www.giantbomb.com/api/documentation#toc-0-38
        '''

        params = {"offset": offset,
                  "query": urllib.quote(query, '').replace('-', '%2D')}
        if resources is not None:
            params['resources'] = resources
        if gbfilter is not None:
            params['filter'] = gbfilter
        if limit is not None:
            params['limit'] = limit

        url = self._build_url("search", params=params)

        results = simplejson.load(urllib2.urlopen(url))
        return [SearchResult(x)
                for x in check_response(results)]

    def get_video(self, gbid):
        '''
        Get a video
        http://www.giantbomb.com/api/documentation#toc-0-44
        '''

        if not isinstance(gbid, int):
            gbid = gbid.id
        url = self._build_url('video/%s' % gbid)
        video = simplejson.load(urllib2.urlopen(url))
        return Video(check_response(video))


def update(obj, args):
    '''Update an objects dictionary using args'''

    for key, value in args.items():
        setattr(obj, key, value)


class SimpleObject(object):
    '''
    A basic object that updates its dictionary using json data or kwargs
    '''

    def __init__(self, json=None, **kwargs):
        if json:
            self.__dict__.update(json)
        self.__dict__.update(kwargs)

    def __repr__(self):
        return Api.default_repr(self)


class Franchise(SimpleObject):
    '''Represents the Franchise Object'''

    pass


class Game(SimpleObject):
    '''Reprensents a Game'''

    def __init__(self, json=None, **kwargs):
        self.platforms = []
        self.json = json

        if json:
            if json.get('platforms'):
                self.platforms = [Platform(plat)
                                  for plat in list(json.pop('platforms', []))]

        if kwargs.get('platforms'):
            self.platforms.extend([Platform(plat) for plat in
                                   list(kwargs.pop('platforms', []))])

        super(Game, self).__init__(json=json, **kwargs)


class Genre(SimpleObject):
    '''Reprensents a Genre'''

    pass


class Image(SimpleObject):
    '''Reprensents an Image'''

    pass


class Platform(SimpleObject):
    '''Reprensents a Platform'''

    _platforms = dict()

    def __init__(self, json=None, **kwargs):
        self.id = None
        self.platforms = []
        self.json = json

        super(Platform, self).__init__(json=json, **kwargs)

        if self.id in self._platforms:
            self = self._platforms[self.id]
        else:
            self._platforms[self.id] = self


class SearchResult(SimpleObject):
    '''Reprensents search results'''

    pass


class Video(SimpleObject):
    '''Reprensents a Video'''

    def __init__(self, json=None, **kwargs):
        self.image = None
        self.json = json

        if json:
            if json.get('image'):
                self.image = Image(json.pop('image', None))

        if kwargs.get('platforms'):
            self.image = Image(kwargs.pop('image', None))

        super(Video, self).__init__(json=json, **kwargs)


class Videos(SimpleObject):
    '''Reprensents multiple videos'''

    def __init__(self, json=None, **kwargs):
        self.image = None
        self.json = json

        if json:
            if json.get('image'):
                self.image = Image(json.pop('image', None))

        if kwargs.get('platforms'):
            self.image = Image(kwargs.pop('image', None))

        super(Videos, self).__init__(json=json, **kwargs)
