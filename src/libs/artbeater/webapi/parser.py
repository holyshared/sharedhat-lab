# coding: utf-8

"""The purser who analyzes the response of api is offered."""

from xml.dom import minidom, Node
from artbeater.webapi.entity import Response

class ResponseParser():

    """Constructor of this class. """

    _multi_element = []

    def __init__(self, elements):
        self._multi_element = elements

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
        elementNumber = 0
        if (element._attrs):
            attrs = element._attrs
            for key, value in attrs.iteritems():
                result[self._toKey(key)] = value.nodeValue
    
        if (element.childNodes):
            for node in element.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    elementNumber += 1
                    #It converts it into the list type when there are two or more elements of the same name.
                    #Element pattern:
                    #    <Image src="" />
                    #    <Image src="" />
                    #    <Image src="" />
                    key = self._toKey(node.nodeName)
                    if not result.has_key(key):
                        result[key] = [self._perseElement(node)] if (key in self._multi_element) else self._perseElement(node)
                    elif isinstance(result[key], list):
                        result[key].append(self._perseElement(node))
                    else:
                        result[key] = [result[key], self._perseElement(node)]
                elif node.nodeType in [Node.TEXT_NODE, Node.CDATA_SECTION_NODE]:
                    if (len(result) > 0 and elementNumber <= 0 and not node.nodeValue.strip() == ''):
                        #When there are an element content and an attribute
                        #Element pattern:
                        #    <Element id="1000">some content</Element>
                        result['content'] = node.nodeValue
                    else:
                        #When there is an element content
                        #Element pattern:
                        #    <Element>some content</Element>
                        if (not node.nodeValue.strip() == ''):
                            return node.nodeValue

        #There is no element content and it only for the attribute
        #Element pattern:
        #    <Element id="1000"></Element>
        if (len(result) > 0 and elementNumber <= 0):
            result['content'] = ''
        elif (len(result) <= 0):
            result = ''

        return result

    def _toKey(self, key):
        return key[0].lower() + key[1:]


if __name__ == '__main__':

    parser = ResponseParser(['event', 'image', 'media'])
    res = parser.parse('../../../test/xml/response.xml')

    for event in res['event']:
        print 'id: ' + event['id']
        print 'href: ' + event['href']

        print 'Name: ' + event['name']
        print 'Venue: tpye=' + event['venue']['type'] + ' name=' + event['venue']['name']

        if (isinstance(event['media'], list)):
            print 'Media: ' + ', ' . join(event['media'])
        else:
            print 'Media: ' + event['media']

        print 'Description: ' + event['description']

        for image in event['image']:
            print image['src']
            print image['width']

        print 'Karma: ' + event['karma']
        print 'Price: ' + event['price']['content']
        print 'Free: ' + event['price']['free']

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
