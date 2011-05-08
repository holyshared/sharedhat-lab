# coding: utf-8

from google.appengine.ext import db

class Response(db.Model):
    hashkey = db.StringProperty()
    query = db.StringProperty()
    name = db.StringProperty()
    cached = db.DateTimeProperty()
    expired = db.DateTimeProperty()
#    content = db.TextProperty()
    content = db.BlobProperty()

"""
class Method(db.Model):
    hashkey = db.StringProperty()
    query = db.StringProperty()
    name = db.StringProperty()
    cached = db.DateTimeProperty()
    expired = db.DateTimeProperty()

class Venue(db.Model):
    name = db.StringProperty()
    type = db.StringProperty()
    address = db.PostalAddressProperty()
    access = db.StringProperty()
    area = db.StringProperty()
    href = db.StringProperty()
    phone = db.PhoneNumberProperty()
    openingHour = db.TimeProperty()
    closingHour = db.TimeProperty()
    scheduleDetails = db.TextProperty()
    scheduleNote = db.TextProperty()

class Event(db.Model):
    id = db.StringProperty()
    method = db.ReferenceProperty(Method)
    venue = db.ReferenceProperty(Venue)
    name = db.StringProperty()
    href = db.StringProperty()
    description = db.TextProperty()
    media = db.StringListProperty()
    image = db.StringListProperty()
    karma = db.FloatProperty()
    price = db.StringProperty()
    position = db.GeoPtProperty()
    distance = db.FloatProperty()
    datum = db.StringProperty()
    dateStart = db.DateProperty()
    dateEnd = db.DateProperty()
    daysBeforeEnd = db.IntegerProperty()
    scheduleNote = db.TextProperty()
    permanentEvent = db.IntegerProperty()
"""