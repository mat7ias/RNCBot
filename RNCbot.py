from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from time import time
from collections import deque
from pathlib import Path
import time
import os
from pprint import pprint
import sys
import yaml
import telegram

#### Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                    '%(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

##### Open config_file
config = None
if os.path.isfile("config.ymal"):
    with open("config.ymal") as config_file:
        config = yaml.load(config_file)
else:
    exit("No configuration file 'config.yaml' found")
    sys.exit()

##### load config
bot_token = config['bot_token']
bot = telegram.Bot(token=bot_token)

# Start message
def start(bot, update):
    update.message.reply_text('Hi! /commands')
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    pprint(update.message.chat.type)

############################ Spam/Flood filter #################################

def sameuser(bot, update):
    user_id = update.message.from_user.id
    previous_user = config['previous_user_id']
    count = config['msg_count']
    spammerid = int
    chat_id = update.message.chat.id
    pprint(update.message.chat.type)

    if (user_id == previous_user) and (update.message.chat.type == 'supergroup'):
        config['msg_count'] = count + 1
        if (count == 5):
	    update.message.reply_text("\xF0\x9F\x8C\x8A")
        if (count >= 6):
            if spammerid != user_id:
                spammerid = user_id
                bot.restrictChatMember(chat_id,
                user_id = spammerid,
                can_send_messages=False,
                until_date=time.time()+int(float(60)*60)) # 60 min restriction
                update.message.reply_text("You're typing at \xE2\x9A\xA1 speed!"
                " My flood filter has turned on to cool off that "
                "\xF0\x9F\x94\xA5 for an hour.")
                pprint('Flooder tripped')
                pprint(spammerid)
            else:
               count = 0
    else:
        count = 0
        config['msg_count'] = count
        config['previous_user_id'] = user_id

################################ Commands ######################################

def commands(bot, update):
    chat_id = update.message.chat.id
    msg = config['commands']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def heybot(bot, update):
    chat_id = update.message.chat.id
    msg = config['heybot']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def resources(bot, update):
    chat_id = update.message.chat.id
    msg = config['resources']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def events(bot, update):
    chat_id = update.message.chat.id
    msg = config['events']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def previousevents(bot, update):
    chat_id = update.message.chat.id
    msg = config['previousevents']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def videos(bot, update):
    chat_id = update.message.chat.id
    msg = config['videos']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def uraiden(bot, update):
    chat_id = update.message.chat.id
    msg = config['uraiden']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def whenmoon(bot, update):
    chat_id = update.message.chat.id
    msg = config['whenmoon']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rules(bot, update):
    chat_id = update.message.chat.id
    msg = config['rules']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminlist(bot, update):
    chat_id = update.message.chat.id
    msg = config['adminlist']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def ignorethat(bot, update):
    chat_id = update.message.chat.id
    msg = config['ignorethat']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def devcon(bot, update):
    chat_id = update.message.chat.id
    msg = config['devcon']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminpolicy(bot, update):
    chat_id = update.message.chat.id
    msg = config['adminpolicy']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def pulse(bot, update):
    chat_id = update.message.chat.id
    msg = config['pulse']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

###############################################################################

###### Error logging
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

###### Running the bot
def main():
    # Create the EventHandler and pass it your bot's token.
    print("Bot started")
    updater = Updater(bot_token)

##### Get the dispatcher to register handlers
    dp = updater.dispatcher

##### CommandHandlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("heybot", heybot))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("events", events))
    dp.add_handler(CommandHandler("previousevents", previousevents))
    dp.add_handler(CommandHandler("videos", videos))
    dp.add_handler(CommandHandler("uraiden", uraiden))
    dp.add_handler(CommandHandler("whenmoon", whenmoon))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("adminlist", adminlist))
    dp.add_handler(CommandHandler("ignorethat", ignorethat))
    dp.add_handler(CommandHandler("devcon", devcon))
    dp.add_handler(CommandHandler("adminpolicy", adminpolicy))
    dp.add_handler(CommandHandler("pulse", pulse))

##### MessageHandlers
    dp.add_handler(MessageHandler(Filters.all, sameuser))

##### Log all errors
    dp.add_error_handler(error)

# Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
