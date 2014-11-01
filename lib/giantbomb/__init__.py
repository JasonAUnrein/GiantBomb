'''
GiantBomb is an interface to the API on giantbomb.com.
'''

__author__ = "Leandro Voltolino <xupisco@gmail.com>"
__version__ = "0.7"

import urllib2
import urllib
import functools
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


class Api(object):
    '''
    The primary interface for the GiantBomb module.  Instantiate this with
    your api key and then call the appropriate methods to access the data
    from the giantbomb servers.
    '''

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://www.giantbomb.com/api/'

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

    def get_item(self, uri, cls, gbid):
        '''
        Generic method to get an item from giantbomb.  Intended to be
        used by the __getattr__ method
        '''

        if not isinstance(gbid, int):
            gbid = gbid.id
        url = self._build_url(uri % gbid)
        resp = simplejson.load(urllib2.urlopen(url))
        new_cls = globals()[cls]
        obj = new_cls(check_response(resp))

        return obj

    def get_items(self, uri, valid_args, cls, *args, **kwargs):
        '''
        Generic method to get an item from giantbomb.  Intended to be
        used by the __getattr__ method
        '''

        params = {}
        idx = 0
        for idx, arg in enumerate(args):
            params[valid_args[idx]] = arg
        for key, value in kwargs.iteritems():
            idx += 1
            params[key] = value
        url = self._build_url(uri, params)
        resp = simplejson.load(urllib2.urlopen(url))
        new_cls = globals()[cls]
        return [new_cls(x) for x in check_response(resp)]

    def __getattr__(self, name):
        '''
        Create a partial call that can be used to call the appropriate method
        with the stored parameters
        '''
        if name.startswith('get_'):
            name = name.split('_', 1)[1]
        if name in self.ITEMS:
            return functools.partial(self.get_item, self.ITEMS[name][0],
                                     self.ITEMS[name][1])
        if name in self.LIST_ITEMS:
            return functools.partial(self.get_items, self.LIST_ITEMS[name][0],
                                     self.LIST_ITEMS[name][1],
                                     self.LIST_ITEMS[name][2])

    ITEMS = {'accessory': ('accessory/%s', 'Accessory'),
             'character': ('character/%s', 'Character'),
             # seems that chat has no data yet
             # 'chat': ('chat/%s', 'Chat'),
             'company': ('company/%s', 'Company'),
             'concept': ('concept/%s', 'Concept'),
             'franchise': ('franchise/%s', 'Franchise'),
             'game': ('game/%s', 'Game'),
             'game_rating': ('game_rating/%s', 'GameRating'),
             'genre': ('genre/%s', 'Genre'),
             'location': ('location/%s', 'Location'),
             'object': ('object/%s', 'Object'),
             'person': ('person/%s', 'Person'),
             'platform': ('platform/%s', 'Platform'),
             'promo': ('promo/%s', 'Promo'),
             'rating_board': ('rating_board/%s', 'RatingBoard'),
             'region': ('region/%s', 'Region'),
             'release': ('release/%s', 'Release'),
             'review': ('review/%s', 'Review'),
             'theme': ('theme/%s', 'Theme'),
             'user_review': ('user_review/%s', 'UserReview'),
             # doesn't seem to be working at this time
             # 'video_type': ('video_type/%s', 'VideoType')}
             'video': ('video/%s', 'Video')}

    LIST_ITEMS = {'accessories': ('accessories', ('field_list', 'limit',
                                                  'offset', 'sort', 'filter'),
                                  'Accessory'),
                  'characters': ('characters', ('field_list', 'limit',
                                                'offset', 'sort', 'filter'),
                                 'Character'),
                  # seems that chat has no data yet
                  # 'chats': ('chats', ),
                  'companies': ('companies', ('field_list', 'limit', 'offset',
                                              'sort', 'filter'),
                                'Companies'),
                  'concepts': ('concepts', ('field_list', 'limit', 'offset',
                                            'sort', 'filter'),
                               'Concepts'),
                  'franchises': ('franchises', ('field_list', 'limit',
                                                'offset', 'sort', 'filter'),
                                 'Franchises'),
                  'games': ('games', ('field_list', 'limit', 'offset',
                                      'platforms', 'sort', 'filter'),
                            'Games'),
                  'game_ratings': ('game_ratings', ('field_list', 'limit',
                                                    'offset', 'sort',
                                                    'filter'),
                                   'GameRatings'),
                  'genres': ('genres', ('field_list', 'limit', 'offset'),
                             'Genres'),
                  'locations': ('locations', ('field_list', 'limit', 'offset',
                                              'sort', 'filter'),
                                'Locations'),
                  'objects': ('objects', ('field_list', 'limit', 'offset',
                                          'sort', 'filter'),
                              'Objects'),
                  'people': ('people', ('field_list', 'limit', 'offset',
                                        'sort', 'filter'),
                             'People'),
                  'platforms': ('platforms', ('field_list', 'limit', 'offset',
                                              'sort', 'filter'),
                                'Platforms'),
                  'promos': ('promos', ('field_list', 'limit', 'offset',
                                        'sort', 'filter'),
                             'Promos'),
                  'rating_boards': ('rating_boards', ('field_list', 'limit',
                                                      'offset', 'sort',
                                                      'filter'),
                                    'RatingBoards'),
                  'regions': ('regions', ('field_list', 'limit', 'offset',
                                          'sort', 'filter'),
                              'Regions'),
                  'releases': ('releases', ('field_list', 'limit', 'offset',
                                            'platforms', 'sort', 'filter'),
                               'Releases'),
                  'reviews': ('reviews', ('field_list', 'limit', 'offset',
                                          'sort', 'filter'),
                              'Reviews'),
                  'themes': ('themes', ('field_list', 'limit', 'offset',
                                        'sort', 'filter'),
                             'Themes'),
                  'types': ('types', ('filter', ), 'Types'),
                  'user_reviews': ('user_reviews', ('field_list', 'game',
                                                    'limit', 'offset', 'sort',
                                                    'filter'),
                                   'UserReviews'),
                  'videos': ('videos', ('field_list', 'limit', 'offset',
                                        'sort', 'filter'),
                             'Videos'),
                  'video_types': ('video_types', ('field_list', 'limit',
                                                  'offset'),
                                  'VideoTypes')}

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
        if kwargs:
            self.__dict__.update(kwargs)

    def __repr__(self):
        return Api.default_repr(self)


for _, VALUE in Api.ITEMS.iteritems():
    globals()[VALUE[1]] = type(VALUE[1], (SimpleObject,), {})
for _, VALUE in Api.LIST_ITEMS.iteritems():
    globals()[VALUE[2]] = type(VALUE[2], (SimpleObject,), {})


class SearchResult(SimpleObject):
    '''Reprensents search results'''

    pass

"""
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


class Image(SimpleObject):
    '''Represents the collection of images in different returns'''

    pass


class Image(SimpleObject):
    '''Represents the collection of images in different returns'''

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
"""
