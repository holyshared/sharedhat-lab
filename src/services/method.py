# coding: utf-8

import artbeater.webapi
from artbeater.webapi import ArtBeat
from models.artbeat import Response
from services.decorator import DataSourceCache

class ServerError(Exception):
    pass

class NotFoundError(Exception):
    pass

class EventSearchNear():

    @DataSourceCache(method='', expires=3600)
    def execute(self, values={}):
        api = ArtBeat()
        try:
            rp = api.eventSearchNear(values=values)
        except artbeater.webapi.ServerError, e:
            raise ServerError, e.message
        except artbeater.webapi.InvalidResponse, e:
            raise ServerError, e.message
        res = rp.getResult()
        if (not res.hasValue('event')):
            raise NotFoundError, 'The corresponding event was not found.'
        return rp
