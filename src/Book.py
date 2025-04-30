class Book:
    def __init__(self, titulo, autor, ano, paginas, preco):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.paginas = paginas
        self.preco = preco

    def __repr__(self):
        return (
            f"Book(titulo={self.titulo!r}, autor={self.autor!r}, "
            f"ano={self.ano!r}, paginas={self.paginas!r}, preco={self.preco!r})"
        )