import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

from src.Book import Book


class NovatecScraper:
    URL = "https://novatec.com.br/lista.php?id=3"
    REGEX_BOOK = re.compile(r"livros/")
    REGEX_AUTHOR = re.compile(r"autores/")
    REGEX_YEAR = re.compile(r"\b(\d{4})\b")
    REGEX_PAGES = re.compile(r"Páginas:\s*(\d+)")
    REGEX_PRICE = re.compile(r"Preço:\s*R\$\s*(\d+,\d{2})")

    def __init__(self):
        self.soup = None
        self.books = []

    def fetch(self):
        html = urlopen(self.URL)
        self.soup = BeautifulSoup(html, "html.parser")

    def parse(self):
        if self.soup is None:
            raise RuntimeError("Fetch must be called before parse.")

    def get_books(self):
        all_fonts = self.soup.find_all("font")
        all_links_fonts = []
        font_from_link = []
        all_titles = []
        all_authors = []
        all_years = []
        all_pages = []
        all_prices = []
        # Pegando todas as fonts, pois nelas estão os dados que precisamos
        for font in all_fonts:
            # Se nossa font tiver um ancora com o href="...livros/..."
            if font.find_all("a", {"href": self.REGEX_BOOK}):
                # Entao adicionamos o link a nossa lista de links
                all_links_fonts.append(font.find_all("a", {"href": self.REGEX_BOOK}))
                # E a font a nossa lista de fonts verificadas
                font_from_link.append(font)
                # Tambem ja adiconamos o titulo do livro a lista de titulos
                all_titles.append(all_links_fonts[-1][0].text)

        # Para cada font em nossa lista de fonts verificadas, pegamos os dados que precisamos
        for font in font_from_link:
            font.find_all("a", {"href": self.REGEX_AUTHOR})
            all_authors.append(font.find_all("a", {"href": self.REGEX_AUTHOR})[0].text)
            all_years.append(re.findall(self.REGEX_YEAR, font.text)[0])
            all_pages.append(re.findall(self.REGEX_PAGES, font.text)[0])
            all_prices.append(re.findall(self.REGEX_PRICE, font.text)[0])

        for i in range(1, 10):
            self.books.append(Book(all_titles[i], all_authors[i], all_years[i], all_pages[i], all_prices[i]))

        print(self.books)