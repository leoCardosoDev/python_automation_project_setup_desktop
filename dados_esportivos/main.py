from selenium import webdriver
from selenium.webdriver.chrome import ChromeDriverManager
from lxml import html
from bs4 import BeautifulSoup

teams_address_A = {
    'juventude': 'juventude/1980',
    'fortaleza': 'fortaleza/2020',
    'vasco': 'vasco-da-gama/1974',
    'cruzeiro': 'cruzeiro/1954',
    'gremio': 'gremio/5926',
    'flamengo': 'flamengo/5981',
    'bahia': 'bahia/1956',
    'corinthians': 'corinthians/1957',
    'internacional': 'internacional/1966',
    'botafogo': 'botafogo/1958',
    'são paulo': 'sao-paulo/1981',
    'sport': 'sport-recife/1959',
    'palmeiras': 'palmeiras/1963',
    'ceará': 'ceara/2001',
    'rb bragantino': 'red-bull-bragantino/1999',
    'atlético mineiro': 'atletico-mineiro/1977',
    'mirassol': 'mirassol/21982',
    'santos': 'santos/1968',
    'vitória': 'vitoria/1962',
    'fluminense': 'fluminense/1961'
}
browser = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
base_api = 'https://www.sofascore.com/api/v1/team/'
end_api = '/top-players/overall'
api ='1981/unique-tournament/325/season/16183'

def choose_team(time:str):
    data_list = []
    cont_url_list = 0
    cont_data_list = 0
    division = input('Qual divisão você quer? (A ou B): ').strip().lower()
    if division == 'a':
        serie = '325'
        id_team = teams_address_A[time.lower()][-4:]
        end_point_25 = '72034' 
    elif division == 'b':
        serie = '390'
    middle_api = '/unique-tournament/{serie}/season/'
    url_25 = base_api + id_team + middle_api + end_point_25 + end_api
    url_list = [url_25]
