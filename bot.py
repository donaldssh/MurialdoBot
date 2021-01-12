import requests
from bs4 import BeautifulSoup
from datetime import date
import telebot
from telebot import types
import sys

bot_token = sys.argv[1]
bot = telebot.TeleBot(token=bot_token)

url = "https://mensamurialdo.it/menu-settimanale/"

page = requests.get(url)
html = page.text

soup = BeautifulSoup(html, "html5lib")

# example "20200110"
today = date.today().strftime("%Y%m%d")

# flag == 0 mensa is closed
flag = 0
if soup.find(id=today):

    # find the current day
    day = soup.find(id=today)

    # for each day extract "primo secondo and contorno"
    menu = day("h3")

    # extract every plates
    plates = day("span")

    # flag == 1 mensa is open
    flag = 1


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton("/primi")
    itembtn2 = types.KeyboardButton("/secondi")
    itembtn3 = types.KeyboardButton("/contorni")
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.reply_to(message, "Scegli una portata:", reply_markup=markup)


@bot.message_handler(commands=["help"])
def send_welcome(message):
    welcome_message = (
        "I dati sono estratti da mensamurialdo.it\n"
        + "@MurialdoBot è stato sviluppato da @Lombax con il contributo di @DanieleFoscarin.\n"
        + "Istruzioni: \n Primi: /primi\n Secondi: /secondi\n Contorni: /contorni"
    )
    bot.reply_to(message, welcome_message)


@bot.message_handler(commands=["primi"])
def send_welcome(message):
    if flag:
        bot.reply_to(message, get_plates_from_index(0))
    else:
        bot.reply_to(message, "mensa chiusa")


@bot.message_handler(commands=["secondi"])
def send_welcome(message):
    if flag:
        bot.reply_to(message, get_plates_from_index(1))
    else:
        bot.reply_to(message, "mensa chiusa")


@bot.message_handler(commands=["contorni"])
def send_welcome(message):
    if flag:
        bot.reply_to(message, get_plates_from_index(2))

    else:
        bot.reply_to(message, "mensa chiusa")


def get_plates_from_index(i):
    plate_name = menu[i].contents[0]
    formatted_plates = plate_name + "\n"
    start = i * 16
    end = 16 * (i + 1)

    # 8 kinds of plates
    for j in range(start, end):
        plate = plates[j]
        formatted_plates += plate.contents[0] + "\n"

    return formatted_plates


while True:
    try:
        bot.polling()

    except Exception:
        time.sleep(15)
