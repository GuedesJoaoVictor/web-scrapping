from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

html = urlopen("https://novatec.com.br/")
soup = BeautifulSoup(html, "html.parser")

regex_livros = re.compile(r"/livros")
regex_qualquercoisa = re.compile(r".*")

all_links = soup.find_all("a", {"href":regex_livros})

print(all_links)

all_titles = []

for link in all_links:
    if link.find("img", {"alt": regex_qualquercoisa}):
        all_titles.append(link.find("img", {"alt": regex_qualquercoisa}).get)

