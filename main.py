import os
import telebot
import cryptocompare
from dotenv import load_dotenv
import json
load_dotenv()
API_KEY = os.getenv('API_KEY')
greeting_words = json.loads(open('greetings.txt','r').read())
bot = telebot.TeleBot(API_KEY)
coin_data = {}
with open('coin_data.json') as fin:
    coin_data = json.load(fin)

@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, 'Hey, wassup?')

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    print(username)    
    bot.send_message(message.chat.id,'Welcome '+username+'! \N{hugging face} \n I will tell you the current price of your favourite crypto coins \U0001FA99 among all other 200 crypto coins!! \U0001F450 \n You can get started by sending the command in following sequence:\n "price coin_name"')
@bot.message_handler(commands=['hello'])
def hello(message):    
    bot.send_message(message.chat.id, 'Hello '+message.from_user.first_name)
def coin_request(message):
    request = message.text.split()
    if request[0].lower() in greeting_words:
        bot.send_message(message.chat.id,'Hello '+message.from_user.first_name+"!")
        return False
    elif request[0].lower() in ['thanks','thank','awesome','super']:
        bot.send_message(message.chat.id,"You're Welcome "+message.from_user.first_name+"! \N{hugging face}" )
    elif len(request) < 2 or request[0].lower() not in ['price']:
        bot.send_message(message.chat.id,"Hmmm! I'm not sure if I understand this...")
        return False
    else:
        return True

@bot.message_handler(func=coin_request)
def send_price(message):
    request = message.text.split()[1].lower()
    if(coin_data.get(request) != None):
        request = coin_data.get(request)
    price = cryptocompare.get_price(request,'INR')
    if price is None:
        bot.send_message(message.chat.id,"Oops! Couldn't find any data for "+request)
    else:
        price = cryptocompare.get_price(request,'INR')[request.upper()]
        bot.send_message(message.chat.id,'Current price of '+request.upper()+' is ₹ '+str(price['INR']))

    
        

bot.polling()