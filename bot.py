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

soup = BeautifulSoup(html,'html5lib')
today = date.today().strftime("%Y%m%d")   # example "20200110"

flag = 0
if soup.find(id=today):   # flag == 0 mensa is closed
    day = soup.find(id=today)  # find the current day
    menu = day('h3')  # for each day extract the "primo secondo e contorno"
    piatti = day('span') # extract every piatto
    flag = 1;

@bot.message_handler(commands=["start"])
def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('/primi')
        itembtn2 = types.KeyboardButton('/secondi')
        itembtn3 = types.KeyboardButton('/contorni')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.reply_to(message, "Scegli una portata:", reply_markup=markup)

@bot.message_handler(commands=["help"])
def send_welcome(message):
        string_to_print="I dati sono estratti da mensamurialdo.it\n"
        string_to_print=string_to_print+"@MurialdoBot è stato sviluppato da @Lombax con il contributo di @DanieleFoscarin.\n"
        string_to_print=string_to_print+"Istruzioni: \n Primi: /primi\n Secondi: /secondi\n Contorni: /contorni"
        bot.reply_to(message, string_to_print)

@bot.message_handler(commands=["primi"])
def send_welcome(message):
    if flag:
    
        string_to_print = find_string_to_print(0)           # 0 -> primi
                
        bot.reply_to(message, string_to_print)
      
    else:
        bot.reply_to(message, 'mensa chiusa')
      
      
@bot.message_handler(commands=["secondi"])
def send_welcome(message):
    if flag:
        
        string_to_print = find_string_to_print(1)           # 1 -> secondi
                
        bot.reply_to(message, string_to_print)
        
    else:
        bot.reply_to(message, 'mensa chiusa')
            
            
@bot.message_handler(commands=["contorni"])
def send_welcome(message):
    if flag:
        
        string_to_print = find_string_to_print(2)           # 2 -> contorni/dolci
                
        bot.reply_to(message, string_to_print)
        
    else:
        bot.reply_to(message, 'mensa chiusa')
        
        
def handle_messages(messages):
    for message in messages:
        file = open("users.txt", "a")
        file.write(message.chat.username+"\n")
        file.close()
   
   
def find_string_to_print(i):
        nome_piatto = menu[i].contents[0]
        string_to_print = nome_piatto+"\n"
        start = i*16
        end = 16*(i+1)
        for j in range(start, end):   # 8 varieta per piatto
            piatto = piatti[j]
            string_to_print = string_to_print + piatto.contents[0]+'\n'
        
        return string_to_print
            
            
while True:
    try:
        bot.set_update_listener(handle_messages)
        bot.polling()   
        
    except Exception:
        time.sleep(15)
