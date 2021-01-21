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

mensa_closed_message = "Mensa chiusa"


def get_date():
    return date.today().strftime("%Y%m%d")


def mensa_is_open():
    return 1 if soup.find(id=get_date()) else 0


def get_plates_from_index(i):
    formatted_plates = ""
    plates = soup.find(id=get_date()).find_all(class_="col")[i].find_all("span")
    for plate in plates:
        formatted_plates += str(plate.text) + "\n"

    return formatted_plates


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
    if mensa_is_open():
        bot.reply_to(message, get_plates_from_index(0))
    else:
        bot.reply_to(message, mensa_closed_message)


@bot.message_handler(commands=["secondi"])
def send_welcome(message):
    if mensa_is_open():
        bot.reply_to(message, get_plates_from_index(1))
    else:
        bot.reply_to(message, mensa_closed_message)


@bot.message_handler(commands=["contorni"])
def send_welcome(message):
    if mensa_is_open():
        bot.reply_to(message, get_plates_from_index(2))
    else:
        bot.reply_to(message, mensa_closed_message)


while True:
    try:
        bot.polling()

    except Exception:
        time.sleep(15)
