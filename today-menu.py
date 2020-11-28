# dipendenze:
# pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
from datetime import date
import sys

url = "https://mensamurialdo.it/menu-settimanale/"

page = requests.get(url)
html = page.text

soup = BeautifulSoup(html,'html5lib')

today = date.today().strftime("%Y%m%d")   # example "20200110"

flag = 0
if soup.find(id=today):   # flag == 0 se la mensa e' chiusa
    day = soup.find(id=today)  # find the current day
    menu = day('h3')  # for each day extract the "primo secondo e contorno"
    piatti = day('span') # extract every piatto
    flag = 1;

if flag == 0:
    print(date.today().strftime("%d-%m-%Y") + " mensa chiusa")
    sys.exit(0)


for i in range(3):   # primo secondo e contorno
    nome_piatto = menu[i].contents[0]
    print(nome_piatto)

    start = i*16
    end = 16*(i+1)
    for j in range(start, end):   # 8 varieta per piatto
        piatto = piatti[j]
        print(piatto.contents[0])
        

