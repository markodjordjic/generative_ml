import requests
import bs4

class GenericScraper:

    def __init__(self, page: str = None) -> None:
        self.page = page
        self._page_content = None

    def scrape_page(self) -> None:
        self._page_content = requests.get(self.page, timeout=30)

    def get_content(self):

        return self._page_content.content
    

class WikiScraper(GenericScraper):

    def __init__(self, page: str = None) -> None:
        super().__init__(page)
        self.page = page

    

