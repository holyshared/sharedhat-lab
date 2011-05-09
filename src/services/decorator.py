# coding: utf-8

#from hashlib import md5
#from datetime import datetime, timedelta, date, time
import pickle
from hashlib import md5
from functools import wraps
from datetime import datetime, timedelta
from models.artbeat import Response
from artbeater.webapi.entity import Response as APIResponse

def DataSourceCache(method, expires=3600):

    def _cacher(function):

        @wraps(function)
        def __cacher(self, **keywords):

            if (not keywords):
                raise TypeError, 'Please specify the argument.'

            request = keywords['values']
            expiresTime = keywords['expires'] if (keywords.has_key('expires')) else expires 

            query = '&'.join([key + '=' + str(request[key]) for key in sorted(request.keys())])

            cache = _getCache(query)
            if (not cache == False):
                return cache

            rp = function(self, request)

            res = rp.getResult()
            content = res.toDictionary()

            _saveCache(key=query, method=method, expires=expiresTime, content=content)

            return res

        return __cacher

    def _saveCache(key, method, expires=3600, content={}):
        content = pickle.dumps(content, pickle.HIGHEST_PROTOCOL)
        cached = datetime.now()
        values = {
            'hashkey': md5(key).hexdigest(),
            'query': key,
            'name': method,
            'cached': cached,
            'expired': cached + timedelta(seconds=expires),
            'content': content
        }
        rp = Response()
        [setattr(rp, key, values[key]) for key in Response.fields().keys()]
        rp.put()

    def _getCache(key):

        rp = Response.all()
        rp.filter('hashkey = ', md5(key).hexdigest())
        res = rp.get()

        if (not res == None):
            content = pickle.loads(res.content)
            rsp = APIResponse(content)

        return rsp if (not res == None) else False

    return _cacher
