'''
See http://www.usps.com/webtools/htm/Address-Information.htm for complete documentation of the API
'''

import urllib, urllib2
try:
    from xml.etree import ElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET

def utf8urlencode(data):
    ret = dict()
    for key, value in data.iteritems():
        ret[key] = value.encode('utf8')
    return urllib.urlencode(ret)

def dicttoxml(dictionary, parent, tagname, attributes=None):
    element = ET.SubElement(parent, tagname)
    if attributes: #USPS likes things in a certain order!
        for key in attributes:
            ET.SubElement(element, key).text = dictionary.get(key, '')
    else:
        for key, value in dictionary.iteritems():
            ET.SubElement(element, key).text = value
    return element

def xmltodict(element):
    ret = dict()
    for item in element.getchildren():
        ret[item.tag] = item.text
    return ret

class USPSXMLError(Exception):
    def __init__(self, element):
        self.info = xmltodict(element)
        super(USPSXMLError, self).__init__(self.info['Description'])

class USPSAddressService(object):
    SERVICE_NAME = None
    API = None
    CHILD_XML_NAME = None
    PARAMETERS = None
    
    def __init__(self, url):
        self.url = url

    def submit_xml(self, xml):
        data = {'XML':ET.tostring(xml),
                'API':self.API}
        response = urllib2.urlopen(self.url, utf8urlencode(data))
        root = ET.parse(response).getroot()
        if root.tag == 'Error':
            raise USPSXMLError(root)
        error = root.find('.//Error')
        if error:
            raise USPSXMLError(error)
        return root
    
    def parse_xml(self, xml):
        items = list()
        for item in xml.getchildren():#xml.findall(self.SERVICE_NAME+'Response'):
            items.append(xmltodict(item))
        return items
    
    def make_xml(self, userid, addresses):
        root = ET.Element(self.SERVICE_NAME+'Request')
        root.attrib['USERID'] = userid
        index = 0
        for address_dict in addresses:
            address_xml = dicttoxml(address_dict, root, self.CHILD_XML_NAME, self.PARAMETERS)
            address_xml.attrib['ID'] = str(index)
            index += 1
        return root
    
    def execute(self, userid, addresses):
        xml = self.make_xml(userid, addresses)
        return self.parse_xml(self.submit_xml(xml))

class AddressValidate(USPSAddressService):
    SERVICE_NAME = 'AddressValidate'
    CHILD_XML_NAME = 'Address'
    API = 'Verify'
    PARAMETERS = ['FirmName',
                  'Address1',
                  'Address2',
                  'City',
                  'State',
                  'Zip5',
                  'Zip4',]
    
class ZipCodeLookup(USPSAddressService):
    SERVICE_NAME = 'ZipCodeLookup'
    CHILD_XML_NAME = 'Address'
    API = 'ZipCodeLookup'
    PARAMETERS = ['FirmName',
                  'Address1',
                  'Address2',
                  'City',
                  'State',]

class CityStateLookup(USPSAddressService):
    SERVICE_NAME = 'CityStateLookup'
    CHILD_XML_NAME = 'ZipCode'
    API = 'CityStateLookup'
    PARAMETERS = ['Zip5',]

