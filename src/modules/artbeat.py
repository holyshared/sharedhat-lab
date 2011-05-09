# coding: utf-8

import modules
from services.method import EventSearchNear

#/artbeat
class MainPage(modules.ModuleHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render('artbeat/index.html')

#/artbeat/event/
class EventPage(modules.ModuleHandler):

    def post(self):

        req = self.request
        lat = req.get('latitude')
        lng = req.get('longitude') 

        api = EventSearchNear()

        try:
            rp = api.execute(values={ 'Latitude': lat, 'Longitude': lng }, expires=3600)
        except URLError, e:
            pass
        except HTTPError, e:
            pass

        eventList = rp.getEvent()
        events = [event.toDictionary() for event in eventList]

        self.response.headers['Content-Type'] = 'text/html'
        self.assign({ 'events': events })
        self.render('artbeat/partials/events.html')
