import unittest

from usps.addressinformation import *

USERID = None

class TestAddressInformationAPI(unittest.TestCase):
    def test_address_validate(self):
        connector = AddressValidate(USPS_CONNECTION_TEST)
        response = connector.execute(USERID, [{'Address2':'6406 Ivy Lane',
                                               'City':'Greenbelt',
                                               'State':'MD'}])[0]
        self.assertEqual(response['Address2'], '6406 IVY LN')
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')
        self.assertEqual(response['Zip4'], '1440')
        
        response = connector.execute(USERID, [{'Address2':'8 Wildwood Drive',
                                               'City':'Old Lyme',
                                               'State':'CT',
                                               'Zip5':'06371',}])[0]
        self.assertEqual(response['Address2'], '8 WILDWOOD DR')
        self.assertEqual(response['City'], 'OLD LYME')
        self.assertEqual(response['State'], 'CT')
        self.assertEqual(response['Zip5'], '06371')
        self.assertEqual(response['Zip4'], '1844')
    
    def test_zip_code_lookup(self):
        connector = ZipCodeLookup(USPS_CONNECTION_TEST)
        response = connector.execute(USERID, [{'Address2':'6406 Ivy Lane',
                                               'City':'Greenbelt',
                                               'State':'MD'}])[0]
        self.assertEqual(response['Address2'], '6406 IVY LN')
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')
        self.assertEqual(response['Zip4'], '1440')
        
        response = connector.execute(USERID, [{'Address2':'8 Wildwood Drive',
                                               'City':'Old Lyme',
                                               'State':'CT',
                                               'Zip5':'06371',}])[0]
        self.assertEqual(response['Address2'], '8 WILDWOOD DR')
        self.assertEqual(response['City'], 'OLD LYME')
        self.assertEqual(response['State'], 'CT')
        self.assertEqual(response['Zip5'], '06371')
        self.assertEqual(response['Zip4'], '1844')
    
    def test_city_state_lookup(self):
        connector = CityStateLookup(USPS_CONNECTION_TEST)
        response = connector.execute(USERID, [{'Zip5':'90210'}])[0]
        self.assertEqual(response['City'], 'BEVERLY HILLS')
        self.assertEqual(response['State'], 'CA')
        self.assertEqual(response['Zip5'], '90210')
        
        response = connector.execute(USERID, [{'Zip5':'20770',}])[0]
        self.assertEqual(response['City'], 'GREENBELT')
        self.assertEqual(response['State'], 'MD')
        self.assertEqual(response['Zip5'], '20770')

if __name__ == '__main__':
    #please append your USPS USERID to test against the wire
    import sys
    USERID = sys.argv.pop()
    unittest.main()
