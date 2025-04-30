from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


html = urlopen("https://novatec.com.br/lista.php?id=3")
soup = BeautifulSoup(html, "html.parser")

# Criando regex para extrair os dados que precisamos.
regex_books = re.compile(r"livros/")
regex_authors = re.compile(r"autores/")
regex_anything = re.compile(r".*")
regex_year = re.compile(r"Ano: \d{4}")
regex_pages = re.compile(r"Páginas: \d+")
regex_price = re.compile(r"Preço: R\$ \d+,\d{2}")

all_fonts = soup.find_all("font")


# Criando variaveis.
all_links_fonts = []
font_from_link = []
all_titles = []
all_authors = []
all_years = []
all_pages = []
all_prices = []


#Pegando todas as fonts, pois nelas estão os dados que precisamos
for font in all_fonts:
    # Se nossa font tiver um ancora com o href="...livros/..."
    if font.find_all("a", {"href": regex_books}):
        # Entao adicionamos o link a nossa lista de links
        all_links_fonts.append(font.find_all("a", {"href": regex_books}))
        #E a font a nossa lista de fonts verificadas
        font_from_link.append(font)
        # Tambem ja adiconamos o titulo do livro a lista de titulos
        all_titles.append(all_links_fonts[-1][0].text)

#Para cada font em nossa lista de fonts verificadas, pegamos os dados que precisamos
for font in font_from_link:
    font.find_all("a", {"href": regex_authors})
    all_authors.append(font.find_all("a", {"href": regex_authors})[0].text)
    all_years.append(re.findall(regex_year, font.text)[0])
    all_pages.append(re.findall(regex_pages, font.text)[0])
    all_prices.append(re.findall(regex_price, font.text)[0])

# Variavel livros para armazenar os 10 livros da primeira pagina.
books = []

# Adicionamos dados a variavel livros.
for i in range(1, 10):
    books.append({
        "titulo": all_titles[i],
        "autor": all_authors[i],
        "ano": all_years[i],
        "paginas": all_pages[i],
        "preco": all_prices[i]
    })

for book in books:
    print(f"Titulo: {book.get("titulo")}")
    print(f"Autor: {book.get("autor")}")
    print(f"Ano: {book.get("ano")}")
    print(f"Paginas: {book.get("paginas")}")
    print(f"Preco: {book.get("preco")}")
    print("------------------------------")