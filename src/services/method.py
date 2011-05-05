# coding: utf-8

from hashlib import md5
from datetime import datetime, timedelta
from artbeater.webapi import ArtBeat
from models.artbeat import Method, Venue, Event

class EventSearchNear():

    _method_name = 'event_search_near'

    _eventProperties = ['id', 'href', 'name', 'medias', 'description', 'images' 'karma',
        'price', 'dateStart', 'dateEnd', 'scheduleNote', 'daysBeforeEnd', 'permanentEvent',
        'distance', 'datum', 'position']

    _venueProperties = ['name', 'type', 'address', 'access', 'area', 'href', 'phone',
        'openingHour', 'closingHour', 'scheduleDetails', 'scheduleNote']

    def find(self, values={}, expires=3600):

        api = ArtBeat()
        response = api.eventSearchNear(values=values, expires=expires)

        req = response.getRequest()
        res = response.getResult()

        result = self.__getCache(str(md5(req.toQueryString())))

        if (result == False):
            result = self.__responseCache(req.toQueryString(), res, expires)

        return result

    def __getCache(self, hashkey):

        query = Method.all()
        query.filter('hashkey = ', hashkey)
        query.filter('expired <= ', datetime.now())
        method = query.get()

        if (method == None):
            return None

        query = Event.all()
        query.filter('method = ', method)
        return query.gets()

    def __responseCache(self, query, response, expires):
        method = self.__createMethod(query=query, expires=expires)
        events = self.__createEvents(response.getEvent())
        for event in events:
            event.method = method
            event.put()

        return events

    def __createMethod(self, query, expires=3600):

        cached = datetime.now()
        method = Method()
        method.hashkey = str(md5(query))
        method.query = query
        method.name = self._method_name
        method.cached = cached
        method.expired = cached + timedelta(seconds=expires)
        method.put()
        return method

    def __createEvents(self, events):
        models = [self.__createEvent(event.toDictionary()) for event in events]
        return models

    def __createEvent(self, event):
        model = Event()
        for key in self._eventProperties:
            if (key == 'position'):
                setattr(model, key, ''.join([event['latitude'], ',' , event['longitude']]))
            else:
                setattr(model, key, event[key])

        model.venue = self.__createVenue(event.venue)

        return model

    def __createVenue(self, venue):

        model = Venue()
        [setattr(model, key, venue[key]) for key in self._venueProperties]
        model.put()

        return model
