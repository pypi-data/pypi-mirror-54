from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

import telebot

config = Config.getConfig(parentKey='modules', key='ht_telegram')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

global bot
bot = ''

class StartModule():

	def __init__(self, token):
		global bot
		bot = telebot.TeleBot(token)

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_telegram'), debug_module=True)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(self, message):
	global bot
	bot.reply_to(message, "Hi! What's up!!")