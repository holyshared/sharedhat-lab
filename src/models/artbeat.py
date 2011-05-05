# coding: utf-8

from google.appengine.ext import db

class Method(db.Model):
    hashkey = db.StringProperty()
    query = db.StringProperty()
    name = db.StringProperty()
    cached = db.DateTimeProperty()
    expired = db.DateTimeProperty()

class Venue(db.Model):
    name = db.TextProperty()
    type = db.StringProperty()
    address = db.PostalAddressProperty()
    access = db.TextProperty()
    area = db.StringProperty()
    href = db.LinkProperty()
    phone = db.PhoneNumberProperty()
    openingHour = db.TimeProperty()
    closingHour = db.TimeProperty()
    scheduleDetails = db.TextProperty()
    scheduleNote = db.TextProperty()

class Event(db.Model):
    id = db.StringProperty()
    method = db.ReferenceProperty(Method)
    venue = db.ReferenceProperty(Venue)
    name = db.TextProperty()
    href = db.StringProperty()
    description = db.TextProperty()
    medias = db.StringListProperty()
    images = db.StringListProperty()
    karma = db.FloatProperty()
    price = db.TextProperty()
    position = db.GeoPtProperty()
    distance = db.FloatProperty()
    datum = db.StringProperty()
    dateStart = db.DateProperty()
    dateEnd = db.DateProperty()
    daysBeforeEnd = db.IntegerProperty()
    scheduleNote = db.TextProperty()
    permanentEvent = db.IntegerProperty()

#method = Method()
#method.key = ''
#method.query = ''
#method.name = 'event_search_near'
#method.cached = '2010-10-10 10:10:10'
#method.expired = '2010-10-10 10:10:10'

#venue = Venue()
#venue.name = ''
#venue.type = ''
#venue.address = ''
#venue.access = ''
#venue.area = ''
#venue.url = ''
#venue.phone = ''
#venue.openingHour = ''
#venue.closingHour = ''
#venue.scheduleDetails = ''
#venue.scheduleNote = ''

#event = EventSearchNear()
#id = db.StringProperty()
#method = db.ReferenceProperty(Method)
#venue = db.ReferenceProperty(Venue)
#name = db.TextProperty()
#url = db.StringProperty()
#description = db.TextProperty()
#medias = db.ListProperty()
#images = db.ListProperty()
#karma = db.FloatProperty()
#price = db.TextProperty()
#position = db.GeoPtProperty()
#distance = db.FloatProperty()
#datum = db.StringProperty()
#dateStart = db.DateProperty()
#dateEnd = db.DateProperty()
#daysBeforeEnd = db.IntegerProperty()
#scheduleNote = db.TextProperty()
#permanentEvent = db.IntegerProperty()












#obj1 = FirstModel()
#obj1.prop = 42
#obj1.put()

#obj2 = SecondModel()

#obj2.reference = obj1.key()

#obj2.reference = obj1
#obj2.put()