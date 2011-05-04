# coding: utf-8

import modules
from artbeater.webapi import ArtBeat

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

        self.response.headers['Content-Type'] = 'text/html'

        artbeat = ArtBeat()
        response = artbeat.eventSearchNear(values={ 'Latitude': lat, 'Longitude': lng }, expires=3600)

        eventList = response.getResult().getEvent()
        events = [event.toDictionary() for event in eventList]

        self.assign({ 'events': events })
        self.render('artbeat/partials/events.html')
