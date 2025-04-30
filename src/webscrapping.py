from src.NovatecScraper import NovatecScraper


def user_selecton(books):
    message = (
        "Digite como você deseja listar os livros:\n"
        " 1 - Listar os por ano.\n"
        " 2 - Listar por nomes.\n"
        " 3 - Listar por preços.\n"
        " 4 - Listar por número de páginas.\n"
        " 5 - Listar por autores.\n"
        "Opção: "
    )
    op = input(message).strip()

    if op == "1":
        ordenados = sorted(books, key=lambda b: b.ano)
        print("\nLivros por ano:")
    elif op == "2":
        ordenados = sorted(books, key=lambda b: b.titulo)
        print("\nLivros por título:")
    elif op == "3":
        ordenados = sorted(books, key=lambda b: float(b.preco.replace(',', '.')))
        print("\nLivros por preço:")
    elif op == "4":
        ordenados = sorted(books, key=lambda b: int(b.paginas))
        print("\nLivros por número de páginas:")
    elif op == "5":
        ordenados = sorted(books, key=lambda b: b.autor)
        print("\nLivros por autor:")
    else:
        print("Opção inválida.")
        return

    for book in ordenados:
        print(f"Título:  {book.titulo}")
        print(f"Autor:   {book.autor}")
        print(f"Ano:     {book.ano}")
        print(f"Páginas: {book.paginas}")
        print(f"Preço:   R$ {book.preco}")
        print("-" * 50)


if __name__ == '__main__':
    scrap = NovatecScraper()
    scrap.fetch()
    scrap.parse()
    # Popula scraper.books via get_books()
    scrap.get_books()
    # Usa a lista de livros retornada em scrap.books
    books = scrap.books
    user_selecton(books)
