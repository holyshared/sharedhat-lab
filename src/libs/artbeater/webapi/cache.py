# coding: utf-8

"""
The manager and the cache object to cache the response when api is executed are offered. 
"""

from datetime import datetime, timedelta

class CacheManager(object):

    """
    The function to cache the response when api is executed is offered. 
    This class is Singleton.

    >>> cacheManager = CacheManager()
    >>> cacheManager.addCache('new-cache-key', Cache(content='some content', expires=3600))
    """

    __caches = {}

    def hasCache(self, key):
        """The existence of cash is confirmed."""
        return self.__caches.has_key(key)

    def getCache(self, key):
        """The cache object is returned based on the key to cash."""
        return self.__caches[key] if (self.hasCache(key)) else False

    def addCache(self, key, cache):
        """Cash is stored based on the key."""
        self.__caches[key] = cache;

    def removeCache(self, key):
        """Cash is deleted based on the key."""
        del self.__caches[key]

    def clearCache(self):
        """All cash is deleted."""
        self.__caches.clear()

    def getLength(self):
        """The number of cash is changed."""
        return len(self.__caches.keys())

    def __new__(cls, *args, **keywords):
        if not hasattr(cls, '_instance'):
            orig = super(CacheManager, cls)
            cls._instance = orig.__new__(cls, *args, **keywords)

        return cls._instance


class Cache(object):

    """
    This class is a cash class. 
    Effective time of cached contents and cash is done and it does. 

    The cash validity term of default is one hour.

    >>>cacheContent = { 'id': 1, 'name': 'foo bar' }
    >>>cache = Cache(content=cacheContent, expires=3600)
    """

    __content = None
    __expires = 3600
    __limit = 0
    __cached = None

    def __init__(self, content, expires = 3600):

        """
        Constructor of this class. 

        [Arguments]
        1. content(object) - Cached contents
        2. expires(int) - Cached time (second)
        """

        self.__cached = datetime.now()
        self.setExpires(expires)
        self.setContent(content)
        self._calculateCacheExpires()

    def setExpires(self, limit):
        """Effective time of cash is specified at the second."""
        self.__expires = limit
        self._calculateCacheExpires()

    def getExpires(self):
        """Effective time of cash is returned."""
        return self.__expires

    def setContent(self, content):
        """The cash contents are specified."""
        self.__content = content

    def getContent(self):
        """The cash contents is returned."""
        return self.__content;

    def getCacheDateTime(self):
        """The cached time is returned."""
        return self.__cached;

    def getCacheExpiresDateTime(self):
        """Time that cash cuts is returned."""
        return self.__limit;

    def isExpires(self):
        """It is confirmed whether cash is effective."""
        diff = self.getCacheDateTime() - datetime.now()
        if (self.getExpires() < diff.seconds):
            return False
        return True

    def _calculateCacheExpires(self):
        self.__limit = self.__cached + timedelta(seconds=self.getExpires())


if __name__ == '__main__':

    import time

    cache = Cache(expires=3600, content={})
    if (cache.isExpires()):
        print 'valid'

    cache = Cache(expires=1, content={'key1': 1})
    time.sleep(2)
    if (cache.isExpires()):
        print 'valid'
    else:
        print 'invalid'

    manager1 = CacheManager()
    manager1.addCache('firstCache', cache)
    
    saveCache = manager1.getCache('firstCache')
    print saveCache.getContent()

    manager2 = CacheManager()
    print True if (manager2 == manager1) else False

    saveCache = manager2.getCache('firstCache')
    print saveCache.getContent()

    manager1.removeCache('firstCache')
