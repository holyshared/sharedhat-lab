# coding: utf-8

"""
The validation and the cash decorator when api is executed are offered.
"""

from functools import wraps
from hashlib import md5
from artbeater.webapi.cache import CacheManager, Cache

def RequestValidater(function):

    """
    The parameter is verified before the request is transmitted.

    >>> def Mock():
    >>>
    >>>     @RequestValidater
    >>>     def call(self, values)
    >>>         pass
    """

    @wraps(function)
    def _validater(self, **keywords):

        if (not keywords):
            raise TypeError, 'Please specify the argument.'

        request = keywords['values']

        if (not request or not isinstance(request, dict)):
            raise TypeError, 'Please specify the request by the dict type.'

        if (not request.has_key('Latitude')):
            raise ValueError, 'The latitude is not specified.'
        if (not request.has_key('Longitude')):
            raise ValueError, 'The longitude is not specified.'

        return function(self, request)

    return _validater

def ResponseCache(method, expires=3600):

    """
    The response after the request is transmitted is cached.

    >>> def Mock():
    >>>
    >>>     @ResponseCache('method name', expires=3600)
    >>>     def call(self, values)
    >>>         pass
    """

    def _responseCache(function):

        @wraps(function)
        def __responseCache(self, **keywords):
    
            if (not keywords):
                raise TypeError, 'Please specify the argument.'

            request = keywords['values']
            expiresTime = keywords['expires'] if (keywords.has_key('expires')) else expires 

            query = '&'.join([key + '=' + str(request[key]) for key in sorted(request.keys())])
            cacheKey = method + '=' + md5(query).hexdigest()

            cacheManager = CacheManager()
            if (cacheManager.hasCache(cacheKey)):
                cache = cacheManager.getCache(cacheKey)
                if (cache.isExpires()):
                    response = cache.getContent()
                else:
                    response = _responseCached(cacheKey, function(self, request), expiresTime)
            else:
                response = _responseCached(cacheKey, function(self, request), expiresTime)

            return response

        return __responseCache

    def _responseCached(cacheKey, response, expires): 
        if (response.getCode() in [200, 300]):
            cacheManager = CacheManager()
            cacheManager.addCache(cacheKey, Cache(content=response, expires=expires))

        return response

    return _responseCache


if __name__ == '__main__':

    from artbeater.webapi.entity import Response 

    class ValidaterMock():

        @RequestValidater
        def call(self, values={}):
            print 'success'

    class CacheMock():

        @ResponseCache(method='foo', expires=3600)
        def call(self, values={}):
            return Response({
                'code': 200
            })


    class ValidaterAndCacheMock():

        @RequestValidater
        def __prepare(self, values={}):
            return values

        @ResponseCache('foo', expires=3600)
        def call(self, values={}):
            values = self.__prepare(values=values);
            return Response({ 'code': 200 })

    
    method = ValidaterMock()
    try:
        method.call(values={ 'Latitude': 36.5, 'Longitude': 137.8 })
    except ValueError, e:
        print e.message

    try:
        method.call()
    except TypeError, e:
        print e.message

    try:
        method.call('a', 'b')
    except TypeError, e:
        print e.message

    try:
        method.call(['a', 'b'])
    except TypeError, e:
        print e.message

    method = CacheMock()
    try:
        method.call(values={ 'Latitude': 36.5, 'Longitude': 137.8 }, expires=3600)
    except ValueError, e:
        print e.message

    method = ValidaterAndCacheMock();
    method.call(values={ 'Latitude': 36.5, 'Longitude': 137.8 }, expires=1000)
