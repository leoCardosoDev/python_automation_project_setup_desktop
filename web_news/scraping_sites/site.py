import requests
from bs4 import BeautifulSoup

class SiteNoticias:
    def __init__(self, site, header_tags, class_names):
        """
        site: Nome descritivo do site (por exemplo, 'globo', 'uol')
        header_tags: Lista de possíveis tags de cabeçalho que encapsulam os títulos (ex: ['h2', 'h3'])
        class_names: Lista de possíveis nomes de classes que identificam títulos de notícias
        """
        self.site = site
        self.header_tags = header_tags
        self.class_names = class_names
        self.news = []

    def update_news(self, url):
        browsers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        page = requests.get(url, headers=browsers)
        if page.status_code != 200:
            raise Exception(f"Failed to load page from {url}")
        
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')
        noticias = soup.find_all('a')

        # Coletar notícias com base em diferentes tags e classes
        news_dict = {}
        for noticia in noticias:
            for tag in self.header_tags:
                header = noticia.find(tag)
                if header and any(cls in header.get('class', []) for cls in self.class_names):
                    # Armazenar título com link
                    news_dict[header.text] = noticia.get('href')
        self.news = news_dict
