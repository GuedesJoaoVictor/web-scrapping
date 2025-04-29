from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
from urllib.parse import urljoin
import time
from collections import deque

# Configurações
BASE_URL = "https://novatec.com.br"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_soup(url):
    """Cria um objeto BeautifulSoup a partir de uma URL"""
    try:
        req = Request(url, headers=HEADERS)
        html = urlopen(req)
        return BeautifulSoup(html, 'html.parser')
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return None


def extract_book_info(book_element):
    """Extrai informações de um elemento de livro"""
    info = {}

    # Título
    title_elem = book_element.find('h2') or book_element.find('h3') or book_element.find(
        class_=re.compile('title|nome', re.I))
    info['title'] = title_elem.get_text(strip=True) if title_elem else None

    # Link
    link_elem = book_element.find('a', href=True)
    info['url'] = urljoin(BASE_URL, link_elem['href']) if link_elem else None

    # Preço
    price_elem = book_element.find(class_=re.compile('price|preco', re.I))
    info['price'] = price_elem.get_text(strip=True) if price_elem else None

    # Descrição (será extraída quando visitarmos a página do livro)
    info['description'] = None

    return info


def get_related_books(main_url, max_pages=3, max_books=50):
    """Coleta livros principais e relacionados"""
    visited = set()
    books = []
    queue = deque([main_url])

    while queue and len(books) < max_books and len(visited) < max_pages:
        current_url = queue.popleft()

        if current_url in visited:
            continue

        print(f"Processando: {current_url}")
        soup = get_soup(current_url)
        if not soup:
            continue

        visited.add(current_url)

        # Encontra elementos de livros na página atual
        book_elements = soup.find_all(class_=re.compile('product|livro|item', re.I))

        for element in book_elements:
            if len(books) >= max_books:
                break

            book_info = extract_book_info(element)

            if book_info['title'] and book_info['url']:
                # Se for uma página de livro individual, extrai mais detalhes
                if '/livros/' in book_info['url'] and book_info['url'] not in [b['url'] for b in books]:
                    detailed_info = get_book_details(book_info['url'])
                    if detailed_info:
                        book_info.update(detailed_info)
                        books.append(book_info)

                        # Adiciona livros relacionados à fila
                        for related in detailed_info.get('related_books', []):
                            if related['url'] not in visited and related['url'] not in queue:
                                queue.append(related['url'])

                time.sleep(1)  # Delay para evitar sobrecarregar o servidor

    return books


def get_book_details(book_url):
    """Extrai informações detalhadas de uma página de livro"""
    soup = get_soup(book_url)
    if not soup:
        return None

    details = {}

    # Descrição
    description = soup.find('div', class_=re.compile('description|sinopse', re.I))
    details['description'] = description.get_text(strip=True) if description else None

    # ISBN
    isbn = soup.find(string=re.compile('ISBN', re.I))
    details['isbn'] = isbn.find_next().get_text(strip=True) if isbn else None

    # Livros relacionados
    details['related_books'] = []
    related_section = soup.find('h2', string=re.compile('também pode gostar|relacionados', re.I))

    if related_section:
        for item in related_section.find_next_siblings(class_=re.compile('product|livro', re.I), limit=4):
            rel_info = extract_book_info(item)
            if rel_info['title'] and rel_info['url']:
                details['related_books'].append(rel_info)

    return details


# Execução principal
if __name__ == "__main__":
    # Começa pela página principal de livros
    start_url = urljoin(BASE_URL, "/livros/")
    books = get_related_books(start_url, max_pages=5, max_books=30)

    # Filtros
    python_books = [b for b in books if b['title'] and 'python' in b['title'].lower()]
    node_books = [b for b in books if b['title'] and 'node' in b['title'].lower()]

    # Exibir resultados
    print(f"\nTotal de livros coletados: {len(books)}")
    print("\nLivros de Python:")
    for book in python_books:
        print(f"- {book['title']} (Preço: {book.get('price', 'N/A')})")
        print(f"  URL: {book['url']}")
        if book.get('description'):
            print(f"  Descrição: {book['description'][:100]}...")

    print("\nLivros de Node.js:")
    for book in node_books:
        print(f"- {book['title']} (Preço: {book.get('price', 'N/A')})")