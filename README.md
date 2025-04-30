## Documentação do Web Scraping da Novatec

### VISÃO GERAL DO PROJETO
O projeto consiste em um web scraper que extrai informações de livros do site da Novatec, permitindo diferentes visualizações e exportação dos dados. O sistema é composto por três arquivos principais: Book.py, NovatecScraper.py e webscrapping.py.

### ESTRUTURA DO CÓDIGO

#### 1. Book.py
- Classe que representa um livro com seus atributos (título, autor, ano, páginas, preço)
- Implementa __repr__ para representação string do objeto

#### 2. NovatecScraper.py
- Classe responsável pela extração de dados do site
- Utiliza BeautifulSoup para parsing HTML
- Define regex para extração de informações específicas
- Métodos principais: fetch(), parse(), get_books()

#### 3. webscrapping.py
- Script principal que coordena a execução
- Implementa interface de usuário via terminal
- Oferece funcionalidades de ordenação e exportação

### TRATAMENTO DE CASOS OMISSOS

#### 1. Conexão com o Site
- O método fetch() pode falhar se o site estiver indisponível

#### 2. Parsing de Dados
- Método parse() verifica se fetch() foi chamado antes
- Lança RuntimeError se soup não foi inicializado

#### 3. Extração de Dados
- Assume formato específico das informações no HTML
- Limita-se aos primeiros 10 livros (hardcoded)

#### 4. Interface do Usuário
- Validação básica de entrada (apenas dígitos 0-6)
- Tratamento para primeira exportação JSON sem ordenação prévia
- Exportamos para JSON a ultima seleção do usuário, caso ele não tenha escolhido nada, o JSON é ordenado por data.

#### 5. Conversão de Dados
- Trata vírgulas em preços para conversão float
- Assume formato específico de preços (R$ XX,XX)