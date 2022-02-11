import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def parse(react):
    react = react.replace('+', '+%2B+').replace('(', '%28').replace(')', '%29').replace(' ', '').replace('=', '+%3D+')
    response = requests.get(f'https://chemequations.com/ru/?s={react}&ref=input', headers={'User-Agent': UserAgent().chrome})
    response = response.content.decode('UTF-8')
    soup = str(BeautifulSoup(response, 'html.parser'))
    left = soup.find('<title>')
    right = soup[left:].find('Вычисл') - 3 + left
    return soup[left + 7:right]