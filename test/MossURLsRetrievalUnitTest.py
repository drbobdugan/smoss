import unittest
from Config import Config
from MOSSResultsRetriever import MOSSResultsRetriever

class MossURLsTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.validUrl = self.config.getHomevalue()
        self.MossURLsData = MOSSResultsRetriever()

    def test_Valid_URL(self):
        self.assertTrue(self.MossURLsData.get_url(self.validUrl))  # valid URL

    def test_Invalid_URL(self):
        self.assertFalse(self.MossURLsData.get_url("notURL"))  # this is not a valid URL
        self.assertFalse(self.MossURLsData.get_url(1))  # in case file reading goes wrong to this
        self.assertFalse(self.MossURLsData.get_url("http://moss.stanford.edu/results/12121212121212/"))  # 404 not found

#    def test_Invalid_Same_URL(self): #user accidentally entered the same URL. Test should not break the code.
#        self.assertTrue(self.MossURLsData.get_url(self.validUrl))
        # trying to get the information from the same URL will fail
#        self.assertFalse(self.MossURLsData.get_url(self.validUrl))

    def test_Read_URLs_From_Valid_File(self):
        self.assertTrue(self.MossURLsData.get_file_urls("FileInput.txt"))

    def test_Read_URLs_From_Invalid_File(self):
        self.assertFalse(self.MossURLsData.get_file_urls("Invalid"))
        self.assertFalse(self.MossURLsData.get_file_urls(1))

    def test_Number_of_Valid_URLs_Read(self):
        self.MossURLsData.get_file_urls("FileInput.txt")
        self.assertEqual(len(self.MossURLsData.urls), 2)

    def test_Result_Objects(self):
        self.MossURLsData.get_file_urls("FileInput.txt")  # URLs file to parse
        self.assertTrue(self.MossURLsData.get_results())  # checking for errors in the parsing
        self.assertTrue(self.MossURLsData.results)  # checks that it is not null


    def tearDown(self):
        self.MossURLsData = None


def main():
    print("Start")


if __name__ == '__main__':
    unittest.main()
