from src.NovatecScraper import NovatecScraper

if __name__ == '__main__':
    scrap = NovatecScraper()
    scrap.fetch()
    scrap.parse()
    scrap.get_books()