import requests
from bs4 import BeautifulSoup
from datetime import date
import sys

url = "https://mensamurialdo.it/menu-settimanale/"

page = requests.get(url)
html = page.text

soup = BeautifulSoup(html, "html5lib")

today = date.today().strftime("%Y%m%d")

flag = 0
if soup.find(id=today):
    day = soup.find(id=today)
    menu = day("h3")
    plates = day("span")
    flag = 1

if flag == 0:
    print(date.today().strftime("%d-%m-%Y") + " mensa chiusa")
    sys.exit(0)


for i in range(3):
    plate_name = menu[i].contents[0]
    print(plate_name)

    start = i * 16
    end = 16 * (i + 1)
    for j in range(start, end):
        plate = plates[j]
        print(plate.contents[0])
