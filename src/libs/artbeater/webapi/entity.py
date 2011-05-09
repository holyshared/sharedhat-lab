# coding: utf-8

"""
Request object and Response object used in this package are offered.
"""

from types import DictType, ListType
from urllib import urlencode
from urllib2 import Request as UrlLibRequest

def _toGetterMethodName(name):
    return 'get' + name[0].upper() + name[1 : len(name)]

def _toPropertyName(name):
    return name[3].lower() + name[4 : len(name)]

def _createGetter(self, name):
    def handler():
        return self['__' + name]
    return handler

class Entity(dict):

    """
    Getter is made based on the specified data. 
    This object is immutable object.
    """

    def __init__(self, attribs):
        """
        Constructor of this class.

        >>> ent = Entity({ 'key': 100 })
        >>> print ent.getKey()
        """
        self.__instanced = False
        self.__initAccessor(attribs)
        self.__setValues(attribs)
        self.__instanced = True

    def __setitem__(self, key, value):
        if (self.has_key(key) == False and self.__instanced == True):
            raise AttributeError, 'The attribute value cannot be set.'
        return dict.__setitem__(self, key, value)

    def __initAccessor(self, attribs):
        for name in attribs:
            method = _toGetterMethodName(name)
            self.__dict__[method] = _createGetter(self, name)

    def __setValues(self, attribs):
        for key, value in attribs.iteritems():
            self['__' + key] = value

    def hasValue(self, key):
        """It is confirmed whether there is a value."""
        return self.has_key('__' + key)

    def toDictionary(self):
        """It converts it into the dict type."""
        result = {}
        for key, method in self.__dict__.iteritems():
            if (key == '_Entity__instanced'): continue

            value = method()
            if (isinstance(value, Entity)):
                value = value.toDictionary()
            elif (isinstance(value, list)):
                expands = []
                for node in value:
                    if (hasattr(node, 'toDictionary')):
                        expands.append(node.toDictionary())
                    else:
                        expands.append(node)
                value = expands

            result[_toPropertyName(key)] = value
        return result


class Request(Entity):

    __url = ''
    __method = 'GET'
    __values = {}

    def __init__(self, *args, **keywords):
        """
        Constructor of this class.

        >>> res = Request(key=100)
        >>> res = Request({ 'key': 100 })
        """
        attribs = keywords if (len(args) <= 0) else list(args).pop()
        Entity.__init__(self, attribs)

    def __set(self, name, value):
        self['__' + name] = value

    def __get(self, name):
        if (self.has_key('__' + name)):
            return self['__' + name]
        return None

    def setMethod(self, method):
        """The method is set."""
        self.__set('method', method)

    def getMethod(self):
        """The setting method is returned."""
        return self.__get('method')

    def setUrl(self, url):
        """Url is set."""
        self.__set('url', url)

    def getUrl(self):
        """Set url is returned."""
        return self.__get('url')

    def setValue(self, name, value):
        """The parameter of the request is set."""
        values = self.__get('values')
        values[name] = value
        self.__set('values', values)

    def getValue(self, name):
        """The parameter of the request is returned."""
        values = self.__get('values')
        return values[name]

    def setValues(self, values):
        """Two or more parameters of the request are set."""
        [self.setValue(key, value) for key, value in values.iteritems()]

    def getValues(self):
        """All parameters of the request are returned."""
        return self.__get('values')

    def toHTTPRequest(self):
        """urllib2.Request object is returned."""
        query = {}
        if (not self.getValues() == None):
            values = self.getValues()
            for key, value  in values.iteritems():
                query[key[0].upper() + key[1 : len(key)]] = value

        if (self.getMethod() == 'GET'):
            request = UrlLibRequest(self.getUrl() + urlencode(query))
        else:
            request = UrlLibRequest(self.getUrl(), urlencode(query))

        request.add_header('Accept-Encoding', 'gzip, deflate')

        return request

    def toQueryString(self):
        """The query character string is returned."""
        return self.__str__()

    def __str__(self):
        return '&'.join([k + '=' + str(self.getValue(k)) for k in sorted(self.getValues().keys())])


class Response(Entity):

    """Response object of api."""

    def __init__(self, attribs):
        """
        Constructor of this class.

        [Arguments]
        attribs(dict) - Attribute of response object.
        """
        attribs = self._walk(attribs)
        Entity.__init__(self, attribs)

    def _walk(self, values):
        for key, value in values.iteritems():
            if (type(value) is ListType):
                nodes = []
                for item in value:
                    if (isinstance(item, dict)):
                        nodes.append(Response(item)) 
                    else:
                        nodes.append(item) 
                values[key] = nodes
            elif (type(value) is DictType):
                values[key] = Response(value)
        return values


if __name__ == '__main__':

    entityValues = {
        'id': 1,
        'name': 'My name',
        'content': 'Some Content'
    }
    node = Entity(entityValues)

    print 'Node Object=============='
    print node.toDictionary()


    print 'Request Object==========='

    request1 = Request(url='http://example', values=entityValues)

    request1.setValue('lat', 36.15151)
    request1.setValue('lng', 36.15151)
    request1.setValues({ 'key1': 1000 })
    print request1.getUrl()
    print request1.toQueryString()


    print 'Response Object==========='

    response = Response({
        'id': 1,
        'name': 'My name',
        'content': 'Some Content',
        'request': request1,
        'elements': [
            {'key': 1, 'value': 2},
            {'key': 2, 'value': 3},
            {'key': 3, 'value': 4},
            {'key': 4, 'value': 5}
        ],
        'user': {
            'firstName': 'foo',
            'lastName': 'bar',
            'histories': [
                {'loginTime': '2010-01-01'},
                {'loginTime': '2010-01-02'},
                {'loginTime': '2010-01-03'}
            ]
        }
    })

    print response.getId()
    print response.getName()
    print response.getContent()
    print response.getElements()

    print 'getRequest'
    req = response.getRequest()
    print req.toQueryString()


    elements = response.getElements()
    for item in elements:
        print item.getKey()
        print item.getValue()

    user = response.getUser()
    print user.getFirstName()
    print user.getLastName()

    histories = user.getHistories()
    for history in histories:
        print history.getLoginTime()

    print response.toDictionary()

    rp = Response({'id': 1})
    print rp.hasValue('event')

    rp = Response({'event': []})
    print rp.hasValue('event')

