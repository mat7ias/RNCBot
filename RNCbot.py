from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from time import time
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

# Configure Logging

FORMAT = '%(asctime)s -- %(levelname)s -- %(module)s %(lineno)d -- %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger('root')
logger.info("Running "+sys.argv[0])

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

def get_name(user):
        try:
            name = user.first_name
        except (NameError, AttributeError):
            try:
                name = user.username
            except (NameError, AttributeError):
                logger.info("No username or first name")
                return	""
        return name

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
def getid(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    update.message.reply_text(str(update.message.chat.first_name)+" : "+str(update.message.chat.id))

def start(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    if (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        msg = config['pmme']
        bot.sendMessage(chat_id=chat_id,text=msg,reply_to_message_id=message_id, parse_mode="Markdown",disable_web_page_preview=1)
    else:
        msg = config['start']
        update.message.reply_text("Hey "+str(update.message.chat.first_name)+"! Get a list of my commands with /commands")

def commands(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['commands']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def extras(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['extras']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def heybot(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    msg = config['heybot']
    update.message.reply_text("Hey "+str(update.message.from_user.first_name)+"!")

def resources(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['resources']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def events(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['events']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def previousevents(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['previousevents']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def videos(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['videos']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def uraiden(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['uraiden']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def whenmoon(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['whenmoon']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rules(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['rules']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminlist(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['adminlist']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def ignorethat(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['ignorethat']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def devcon(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['devcon']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminpolicy(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    if (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        msg = config['pmme']
        bot.sendMessage(chat_id=chat_id,text=msg,reply_to_message_id=message_id, parse_mode="Markdown",disable_web_page_preview=1)
    else:
        msg = config['adminpolicy']
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def pulse(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['pulse']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def nightly(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['nightly']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def releases(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['releases']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def email(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['email']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def brainbot(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['brainbot']
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
    dp.add_handler(CommandHandler('id', getid))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("extras", extras))
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
    dp.add_handler(CommandHandler("nightly", nightly))
    dp.add_handler(CommandHandler("releases", releases))
    dp.add_handler(CommandHandler("email", email))
    dp.add_handler(CommandHandler("brainbot", brainbot))

##### MessageHandlers
    dp.add_handler(MessageHandler(Filters.all, sameuser))

##### Log all errors
    dp.add_error_handler(error)

# Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
