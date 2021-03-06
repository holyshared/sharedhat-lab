# coding: utf-8

"""
The access function of the api method is offered. 
The access object of the method of each API is generated by using the MethodCreater class, and API is executed. 
"""

import gzip
from StringIO import StringIO
from urllib2 import urlopen, URLError, HTTPError
from xml.parsers.expat import ExpatError
import artbeater.webapi
from artbeater.webapi.entity import Response, Request
from artbeater.webapi.parser import ResponseParser
from artbeater.webapi.decorator import RequestValidater, ResponseCache

class AbstractMethod():

    _request = None

    _multi_element = [],

    def __init__(self, request = None):
        """
        Constructor of this class.

        [Arguments]
        1. request(artbeater.webapi.Request) - Request object
        """
        if not request == None:
            self.setRequest(request)

    def call(self, **keywords):
        """
        The api method is executed.

        This method is an abstraction method.
        It is necessary to do override in the subclass.
        """
        raise NotImplementedError

    def setRequest(self, request):
        """The request is set."""
        self._request = request

    def getRequest(self):
        """The request is returned."""
        return self._request

    def getHTTPRequest(self):
        """The <urllib2.Request> object is returned."""
        return self.getRequest().toHTTPRequest()

    def getResult(self):
        """The result is returned."""
        return self._result

    def setResult(self, result):
        """The result is set. """
        self._result = result

    def send(self, request=None):
        """The request is transmitted and the response object is returned."""
        if (not request == None): self.setRequest(request)

        try:
            response = urlopen(self.getHTTPRequest())
        except URLError:
            raise artbeater.webapi.ServerError, 'There is no response from the server. Please execute it after a while again.'
        except HTTPError:
            raise artbeater.webapi.ServerError, 'There is no response from the server. Please execute it after a while again.'

        if response.info().get('Content-Encoding') == 'gzip':
            file = StringIO(response.read())
            content = gzip.GzipFile(fileobj=file)
        else:
            content = response

        parser = ResponseParser(self._multi_element)
        try:
            result = parser.parse(content)
        except ExpatError:
            raise artbeater.webapi.InvalidResponse, 'Xml not an invalid response was received.'

        return Response({
            'code': response.code,
            'message': response.msg,
            'request': request,
            'headers': response.info(),
            'result': result
        })


class EventSearchNear(AbstractMethod):

    """
    The event of coordinates information is retrieved.

    >>> method = EventSearchNear()
    >>> response = method.call({ 'Latitude': 35.6763, 'Longitude': 139.8105 })
    """

    _method_name = 'event_searchNear'

    _multi_element = [ 'event', 'media', 'image' ]

    _defaults = {
        'Datum': 'world',
        'Schedule': 'current',
        'SearchRange': '500m',
        'Description': '',
        'Free': 0,
        'Language': 'ja',
        'ResultDatum': 'world',
        'MaxResults': 5,
        'SortOrder': 'distance'
    }

    def __getUrl(self):
        return artbeater.webapi.ARTBEAT_API_URL + '/list/' + self._method_name + '/?'

    @RequestValidater
    def __prepare(self, values={}):
        queries = self._defaults.copy()
        queries.update(values)
        return queries

    @ResponseCache(method='event_searchNear', expires=3600)
    def call(self, values={}):

        """The event of coordinates information is retrieved."""

        values = self.__prepare(values=values);

        request = Request(method='GET', url=self.__getUrl(), values=values)
        result = self.send(request)
        if (isinstance(result, URLError) or isinstance(result, HTTPError)):
            return result
        else:
            self.setResult(result)
            return self.getResult()


class MethodCreater():

    """The generation function of the method object is offered."""

    _methods = ['eventSearchNear']

    @classmethod
    def create(self, method, request = None):
        """The method object is generated."""
        if not method in self._methods:
            raise NameError, 'Method ' + method + ' doesn\'t exist.'

        if method == 'eventSearchNear':
            strategy = EventSearchNear(request)

        return strategy

    @classmethod
    def getMethods(self):
        """The list of the support method is returned."""
        return self._methods



if __name__ == '__main__':

    class Mock(AbstractMethod):
        pass

    mockMethod = Mock()
    try:
        mockMethod.call(values={
            'key1': 'value1'
        })
    except NotImplementedError:
        print 'oops!!'


    creater = MethodCreater()
    method = creater.create('eventSearchNear')
    response = method.call(values={ 'Latitude': 35.6763, 'Longitude': 139.8105 }, expires=1000)

    print response.getCode()
    print response.getMessage()

    events = response.getResult().getEvent()
    for event in events:
        print event.getName()
        print event.getDescription()

        price = event.getPrice()
        print price.getFree()
        print price.getContent()
