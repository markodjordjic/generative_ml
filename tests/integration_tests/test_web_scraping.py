import unittest
from utilities.scraping import WikiScraper
from bs4 import BeautifulSoup


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
        content = wiki_scraper.get_content()
        soup = BeautifulSoup(content, 'html.parser')
        #items = soup.find_all(name='table')
        indiatable=soup.find('table',{'class':"wikitable plainrowheaders"})
        import pandas as pd
        table = pd.DataFrame(pd.read_html(str(indiatable)))
        for item in items:
            print(item)
            if 'Medal summary' in item:
                childen = soup.findChildren(item)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestWebScraping('test_wiki_scraper'))

    return suite


if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    runner.run(test_suite())