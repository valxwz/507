import unittest
import proj1_f19 as proj1
import json


class TestMedia(unittest.TestCase):

###test part 1#####
    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")

        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        self.assertEqual(m2.release_year, "No Release Year")

        s1 = proj1.Song("Ocean Eyes", "Billie Eilish", "2017", "Everything")
        self.assertEqual(s1.title, "Ocean Eyes")
        self.assertEqual(s1.author, "Billie Eilish")
        self.assertEqual(s1.release_year, "2017")
        self.assertEqual(s1.album, "Everything")
        self.assertEqual(s1.genra, "No Genra")
        self.assertEqual(s1.track_length, 0)

        mo1 = proj1.Movie("Joker", "Todd Phillips", "2019")
        self.assertEqual(mo1.title, "Joker")
        self.assertEqual(mo1.author, "Todd Phillips")
        self.assertEqual(mo1.release_year, "2019")
        self.assertEqual(mo1.rating, "PG")
        self.assertEqual(mo1.movie_length, 0)

    def testString(self):
        m1 = proj1.Media()
        self.assertEqual(str(m1), "No Title by No Author (No Release Year)")
        s1 = proj1.Song("Ocean Eyes", "Billie Eilish", "2017", "Everything")
        self.assertEqual(str(s1), "Ocean Eyes by Billie Eilish (2017) [No Genra]")
        mo1 = proj1.Movie("Joker", "Todd Phillips", "2019")
        self.assertEqual(str(mo1), "Joker by Todd Phillips (2019) [PG]")

    def testRelativeness(self):
        m1 = proj1.Media()
        self.assertFalse(getattr(m1, 'rating', False))
        s1 = proj1.Song()
        self.assertFalse(getattr(m1, 'rating', False))
        mo1 = proj1.Movie()
        self.assertFalse(getattr(m1, 'album', False))

    def testLen(self):
        m1 = proj1.Media()
        self.assertEqual(len(m1), 0)
        s1 = proj1.Song("Ocean Eyes", "Billie Eilish", "2017", "Everything")
        self.assertTrue(type(len(s1) / 60), int)
        mo1 = proj1.Movie("Joker", "Todd Phillips", "2019")
        self.assertTrue(type(len(s1) / 360), int)

##test part 2####

    def testMedia(self):
        f = open("sample_json.json","r")
        sample_data = json.loads(f.read())
        f.close()
        
        m = proj1.Media(json_dict=sample_data[2])

        self.assertEqual(m.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(m.author, "Helen Fielding")
        self.assertEqual(m.release_year, "2012")
        self.assertEqual(m.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
        self.assertEqual(m.__len__(), 0)

    def testSong(self):
        f = open("sample_json.json","r")
        sample_data = json.loads(f.read())
        f.close()
        
        s = proj1.Song(json_dict=sample_data[1])
        
        self.assertEqual(s.title, "Hey Jude")
        self.assertEqual(s.author, "The Beatles")
        self.assertEqual(s.release_year, "1968")
        self.assertEqual(s.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(s.genra, "Rock")
        self.assertEqual(s.track_length, 431333)
        self.assertEqual(s.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(s.__len__(), 431)


    def testMovie(self):
        f = open("sample_json.json","r")
        sample_data = json.loads(f.read())
        f.close()
        
        mo = proj1.Movie(json_dict=sample_data[0])
        
        self.assertEqual(mo.title, "Jaws")
        self.assertEqual(mo.author, "Steven Spielberg")
        self.assertEqual(mo.release_year, "1975")
        self.assertEqual(mo.rating, "PG")
        self.assertEqual(mo.movie_length, 7451455)
        self.assertEqual(mo.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
        self.assertEqual(mo.__len__(), 124)


###test part 3#####


    def testPartThree(self):
        r1 = proj1.get_from_api("love")
        r2 = proj1.get_from_api("baby")
        r3 = proj1.get_from_api("moana")
        r4 = proj1.get_from_api("helter skelter")

        self.assertIn(len(r1), range(1,11))
        self.assertIn(len(r1), range(1,11))
        self.assertIn(len(r1), range(1,11))
        self.assertIn(len(r1), range(1,11))

        r_nonesense = proj1.get_from_api("&&$@#!")
        r2_nonesense = proj1.get_from_api("asdasdasdasdade")
        self.assertEqual(r_nonesense, [])
        self.assertEqual(r2_nonesense, [])


unittest.main()
