import requests

url = 'https://www.sofascore.com/tournament/football/brazil/brasileirao-serie-a/325#id:72034'
browser = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
page = requests.get(url, headers=browser)

with open('page.html', 'w', encoding='utf-8') as file:
    file.write(page.text)