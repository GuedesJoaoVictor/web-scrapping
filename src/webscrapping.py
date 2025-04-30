import json
from src.NovatecScraper import NovatecScraper


def user_selecton(books):
    message = (
        "Digite como você deseja listar os livros:\n"
        " 1 - Listar por ano.\n"
        " 2 - Listar por nomes.\n"
        " 3 - Listar por preços.\n"
        " 4 - Listar por número de páginas.\n"
        " 5 - Listar por autores.\n"
        " 6 - Salvar em JSON formatado.\n"
        " 0 - Sair.\n"
        "Opção: "
    )

    last_list = None
    last_label = None

    while True:
        op = input(message).strip()
        if op == "1":
            ordenados = sorted(books, key=lambda b: b.ano)
            print("\nLivros por ano:")
            last_list = ordenados
            last_label = 'ano'
        elif op == "2":
            ordenados = sorted(books, key=lambda b: b.titulo)
            print("\nLivros por título:")
            last_list = ordenados
            last_label = 'titulo'
        elif op == "3":
            ordenados = sorted(books, key=lambda b: float(b.preco.replace(',', '.')))
            print("\nLivros por preço:")
            last_list = ordenados
            last_label = 'preco'
        elif op == "4":
            ordenados = sorted(books, key=lambda b: int(b.paginas))
            print("\nLivros por número de páginas:")
            last_list = ordenados
            last_label = 'paginas'
        elif op == "5":
            ordenados = sorted(books, key=lambda b: b.autor)
            print("\nLivros por autor:")
            last_list = ordenados
            last_label = 'autor'
        elif op == "6":
            if last_list is None:
                # nenhuma opção válida antes: salva por ano
                last_list = sorted(books, key=lambda b: b.ano)
                last_label = 'ano'
            filename = f"livros_ordenados_por_{last_label}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json_list = [b.__dict__ for b in last_list]
                json.dump(json_list, f, ensure_ascii=False, indent=4)
            print(f"\nArquivo '{filename}' salvo com sucesso!\n")
            continue
        elif op == "0":
            print("Obrigado por usar nosso algoritmo!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")
            continue

        # exibir lista ordenada
        for book in last_list:
            print(f"Título:  {book.titulo}")
            print(f"Autor:   {book.autor}")
            print(f"Ano:     {book.ano}")
            print(f"Páginas: {book.paginas}")
            print(f"Preço:   R$ {book.preco}")
            print("-" * 50)
        print()
        input("Pressione ENTER para continuar...")


if __name__ == '__main__':
    scrap = NovatecScraper()
    scrap.fetch()
    scrap.parse()
    scrap.get_books()
    books = scrap.books
    user_selecton(books)
