from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


html = urlopen("https://novatec.com.br/lista.php?id=3")
soup = BeautifulSoup(html, "html.parser")

regex_livros = re.compile(r"livros/")
regex_qualquercoisa = re.compile(r".*")

all_fonts = soup.find_all("font")

all_links_fonts = []
font_from_link = []
all_titles = []

for font in all_fonts:
    if font.find_all("a", {"href": regex_livros}):
        all_links_fonts.append(font.find_all("a", {"href": regex_livros}))
        font_from_link.append(font)
        all_titles.append(all_links_fonts[-1][0].text)

print(all_titles)