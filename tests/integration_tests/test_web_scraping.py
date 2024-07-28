import unittest
from utilities.scraping import WikiScraper

class TestWebScraping(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_wiki_scraper(self):

        wiki_scraper = WikiScraper(
            page='https://en.wikipedia.org/wiki/Artistic_swimming_at_the_2024_Summer_Olympics',
        )
        wiki_scraper.scrape_page()
        wiki_scraper.get_content()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestWebScraping('test_find_and_replace'))

    return suite


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(test_suite())