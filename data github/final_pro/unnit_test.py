import unittest
from final_pro import *

class TestGetInfo(unittest.TestCase):


    def test_get_venue_info(self):
        sample_venue_info=get_venue_info(make_request_using_cache(search_url,params))
        # test if the results returned from yelp api is based on the city and state input
        for i in sample_venue_info:
            location_returned=sample_venue_info[i]["location"].split(" ")
            print (location_returned)
            self.assertIn(state.upper(),location_returned)
        
    def test_get_site_location(self):
        sample_site_location=get_site_location("1 n. state str, ann arbor, MI")
        self.assertEqual(sample_site_location, [42.28387170000001, -83.7410453])

class TestInsertFuntion(unittest.TestCase):

    def test_insert_to_competitor(self):
        # check if the place picked from the list is saved in the competitor table
        competitor_picked=insert_to_competitor()
        self.assertIsNotNone(competitor_picked)
    def test_search_parking(self):
        try:
            search_parking("Chicago")
        except:
            self.fail()
    def test_show_map(self):
        search_url = 'https://api.yelp.com/v3/businesses/search'
        # search_url maybe not needed?
        params = {'term':"coffee",'location':"Ann Arbor",'radius':'5000','limit':'15','sort_by':'rating'}
        sample_venue_info=get_venue_info(make_request_using_cache(search_url,params))
        try:
            show_map(sample_venue_info,choosen_site=["1 n. state street, ann arbor, mi"],city="Ann Arbor")
        except:
            self.fail()
    def test_present_song(self):
        try:
            results=present_songs()
        except:
            self.fail()

unittest.main()
