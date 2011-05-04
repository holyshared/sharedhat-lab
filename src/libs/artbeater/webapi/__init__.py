# coding: utf-8

"""
All the api access functions are offered.
"""

from artbeater.webapi.entity import Request
from artbeater.webapi.method import MethodCreater
from artbeater.webapi.cache import CacheManager

ARTBEAT_API_URL = 'http://www.tokyoartbeat.com'

class ArtBeat():

    """
    This class offers all the api methods.

    >>> artbeat = ArtBeat()
    >>> response = artbeat.eventSearchBear({ 'Latitude': 35.6763, 'Longitude': 139.8105 })
    >>> events = response.getResult().getEvent()
    >>> for event in events:
    >>>     print event.getName()
    >>>     print event.getDescription()
    >>>     venue = event.getVenue()
    >>>     print venue.getName()
    >>>     print venue.getType()
    """

    def __init__(self):

        """Constructor of this class."""       

        self._creater = MethodCreater()
        for method in self._creater.getMethods():
            self.__dict__[method] = self._createMethod(method)

    def _createMethod(self, method):

        def _method(**keywords):
            try:
                strategy = self._creater.create(method)
            except NameError:
                print NameError

            response = strategy.call(**keywords)

            return response

        return _method


if __name__ == '__main__':

    artbeat = ArtBeat()
    response = artbeat.eventSearchNear(values={ 'Latitude': 35.6763, 'Longitude': 139.8105 })

    events = response.getResult().getEvent()
    for event in events:
        print event.getName()
        print event.getDescription()
        venue = event.getVenue()
        print venue.getName()
        print venue.getType()

    response = artbeat.eventSearchNear(values={ 'Latitude': 35.6763, 'Longitude': 139.8105 })
