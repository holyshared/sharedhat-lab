# coding: utf-8

"""The purser who analyzes the response of api is offered."""

from xml.dom import minidom, Node
from artbeater.webapi.entity import Response

class ResponseParser():

    """Constructor of this class. """

    def parse(self, file):
        """The content is read, analyzed from the file, and the dictionary object is returned."""
        document = minidom.parse(file);
        return self._perseElement(document.documentElement)

    def parseString(self, content):
        """The character string is analyzed and the dictionary object is returned."""
        document = minidom.parseString(content);
        return self._perseElement(document.documentElement)

    def _perseElement(self, element):

        result = {}
        if (element._attrs):
            attrs = element._attrs
            for key, value in attrs.iteritems():
                result[self._toKey(key)] = value.nodeValue
    
        if (element.childNodes):
            for node in element.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    key = self._toKey(node.nodeName)
                    if not result.has_key(key):
                        result[key] = self._perseElement(node)
                    elif isinstance(result[key], list):
                        result[key].append(self._perseElement(node))
                    else:
                        result[key] = [result[key], self._perseElement(node)]
                elif node.nodeType in [Node.TEXT_NODE, Node.CDATA_SECTION_NODE]:
                    if (not node.nodeValue.strip() == ''):
                        return node.nodeValue

        return result

    def _toKey(self, key):
        return key[0].lower() + key[1:]


if __name__ == '__main__':

    parser = ResponseParser()
    res = parser.parse('../../../test/xml/response.xml')

    for event in res['event']:
        print 'id: ' + event['id']
        print 'href: ' + event['href']

        print 'Name: ' + event['name']
        print 'Venue: tpye=' + event['venue']['type'] + ' name=' + event['venue']['name']
        print 'Media: ' + ', '.join(event['media']) 
        print 'Description: ' + event['description']

        for image in event['image']:
            print image['src']
            print image['width']

        print 'Karma: ' + event['karma']
        print 'Price: ' + event['price']
        print 'DateStart: ' + event['dateStart']
        print 'DateEnd: ' + event['dateEnd']
        print 'DaysBeforeEnd: ' + event['daysBeforeEnd']
        print 'PermanentEvent: ' + event['permanentEvent']
        print 'Distance: ' + event['distance']
        print 'Datum: ' + event['datum']
        print 'Latitude: ' + event['latitude']
        print 'Longitude: ' + event['longitude']
        
    response = Response(res)
    print response.getEvent()
