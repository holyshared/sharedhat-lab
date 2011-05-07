# coding: utf-8

from hashlib import md5
from datetime import datetime, timedelta, date, time
#from artbeater.webapi import ArtBeat
from models.artbeat import Method, Venue, Event

class APICacher():

    def get(self, hashkey):
        pass

    def save(self, query, response, expires=3600):
        pass

    def _createMethod(self, query, expires=3600):
        cached = datetime.now()
        method = Method()
        method.hashkey = md5(query).hexdigest()
        method.query = query
        method.name = self._method_name
        method.cached = cached
        method.expired = cached + timedelta(seconds=expires)
        method.put()
        return method


class EventSearchNear(APICacher):

    """
    cacher = EventSearchNear()
    cacher.save('key1=value&key2=values', events, expires=3600)

    cacher = EventSearchNear()
    cacher.get('key1=value&key2=values')
    """

    _method_name = 'event_search_near'

    _eventProperties = ['id', 'href', 'name', 'media', 'description', 'image', 'karma',
        'price', 'dateStart', 'dateEnd', 'scheduleNote', 'daysBeforeEnd', 'permanentEvent',
        'distance', 'datum', 'position']

    _venueProperties = ['name', 'type', 'address', 'access', 'area', 'href', 'phone',
        'openingHour', 'closingHour', 'scheduleDetails', 'scheduleNote']

    def get(self, hashkey):

        query = Method.all()
        query.filter('hashkey = ', hashkey)
        query.filter('expired <= ', datetime.now())
        method = query.get()

        if (method == None):
            return None

        query = Event.all()
        query.filter('method = ', method)
        return query.gets()

    def save(self, query, response, expires=3600):
        method = self._createMethod(query=query, expires=expires)
        events = self.__createEvents(response.getEvent())
        for event in events:
            event.method = method
            event.put()
        return events

    def __createEvents(self, events):
        models = [self.__createEvent(event.toDictionary()) for event in events]
        return models

    def __createEvent(self, event):
        model = Event()
        for key in self._eventProperties:
            if (key == 'position'):
                setattr(model, key, ''.join([event['latitude'], ',' , event['longitude']]))
            elif (key == 'image'):
#                images = [image['src'] for image in event['image']]
#                setattr(model, key, images)
                if (not isinstance(event['image'], list)):
                    event['image'] = [event['image']]
                images = [image['src'] for image in event['image']]
                setattr(model, key, images)
            elif (key == 'media'):
                if (not isinstance(event['media'], list)):
                    event['media'] = [event['media']]
                medias = [media for media in event['media']]
                setattr(model, key, medias)
            elif (key in ['karma', 'distance']):
                setattr(model, key, float(event[key]))
            elif (key == 'price'):
                setattr(model, key, event[key]['content'])
            elif (key in ['dateStart', 'dateEnd']):
                y, m, d = event[key].split('-')
                setattr(model, key, date(year=int(y),month=int(m),day=int(d)))
            elif (key in ['permanentEvent', 'daysBeforeEnd']):
                setattr(model, key, int(event[key]))
            else:
                setattr(model, key, event[key])

        model.venue = self.__createVenue(event['venue'])

        return model

    def __createVenue(self, venue):

        model = Venue()
        for key in self._venueProperties:
            if (key == 'area'):
                setattr(model, key, venue[key]['content'])
            elif (key in ['openingHour', 'closingHour']):
                h, m, s = venue[key].split(':')
                setattr(model, key, time(hour=int(h),minute=int(m),second=int(s)))
            else:
                setattr(model, key, venue[key])
        model.put()

        return model
