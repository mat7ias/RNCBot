from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time
import os
from pprint import pprint
import sys
import yaml
import telegram
import random

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
if os.path.isfile("bot/RaidenBot/config.yaml"):
    with open("bot/RaidenBot/config.yaml") as config_file:
        config = yaml.load(config_file)
else:
    exit("No configuration file 'config.yaml' found")
    sys.exit()

##### load config
bot_token = config['bot_token']
bot = telegram.Bot(token=bot_token)

ADMINS = config['ADMINS']
MENTIONTEAM = config['MENTIONTEAM']

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
                count = 0
    else:
        count = 0
        config['msg_count'] = count
        config['previous_user_id'] = user_id

############################### New Member #####################################

def new_chat_member(bot, update):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    tag = update.message.from_user.username
    name = get_name(update.message.from_user)
    if (len(name) < 21) and (update.message.chat.type == 'supergroup'):
        bot.restrict_chat_member(chat_id=chat_id,user_id=user_id,until_date=(time.time()+int(float(6000)*6000)),can_send_messages=True,can_send_media_messages=False,can_send_other_messages=False,can_add_web_page_previews=False)
        pprint('New Member')
        bot.delete_message(chat_id=chat_id,message_id=message_id)
        if tag != None:
            msg = ("Welcome @"+str(tag)+"! Check out our [Pinned Post](https://t.me/RaidenNetworkCommunity/2) and community [Discord](https://discord.gg/zZjYJ6e) for feeds on all things Raiden\xE2\x9A\xA1")
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        else:
            msg = ("Welcome "+str(name)+"! Check out our [Pinned Post](https://t.me/RaidenNetworkCommunity/2) and community [Discord](https://discord.gg/zZjYJ6e) for feeds on all things Raiden\xE2\x9A\xA1")
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
    else:
        bot.restrict_chat_member(chat_id=chat_id,user_id=user_id,until_date=(time.time()+int(float(6000)*6000)),can_send_messages=True,can_send_media_messages=False,can_send_other_messages=False,can_add_web_page_previews=False)
        pprint('New Member Long Name')
        bot.delete_message(chat_id=chat_id,message_id=message_id)

################################ Commands ######################################

def getid(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    update.message.reply_text(str(update.message.from_user.first_name)+" : "+str(update.message.from_user.id))

def start(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    if (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        msg = config['pmme']
        bot.sendMessage(chat_id=chat_id,text=msg,reply_to_message_id=message_id, parse_mode="Markdown",disable_web_page_preview=1)
    else:
        msg = config['start']
        update.message.reply_text("Hey "+str(update.message.chat.first_name)+"! I'm a resource bot, message me here or in @RaidenNetworkCommunity telegram group.\n\nGet a list of my commands with /commands")

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

def community(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['community']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def platforms(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['platforms']
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

def conferences(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['conferences']
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

def tokenmodel(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['tokenmodel']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminlist(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['adminlist']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def ignorethat(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    update.message.reply_text("I'm not sure I want to ignore that, "+str(update.message.from_user.first_name)+"...")

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

def RemindMeIn5Years(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    update.message.reply_text("Setting a reminder for "+str(update.message.from_user.first_name)+" 5 years from now.")

def disclaimer(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['disclaimer']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rapps(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['rapps']
    bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def lefteris(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    lefterislist=["/home/ubuntu/lefteris.jpg", "/home/ubuntu/lefteris2.jpg"]
    bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(lefterislist), "rb"))

def meme(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    memelist=["/home/ubuntu/meme.mp4", "/home/ubuntu/meme3.mp4", "/home/ubuntu/meme6.mp4", "/home/ubuntu/meme7.mp4", "/home/ubuntu/meme8.mp4"]
    bot.sendVideo(chat_id=chat_id,timeout=13, video=open(random.choice(memelist), "rb"))

def weeklyupdate(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if (user_id in ADMINS) or (user_id in MENTIONTEAM):
        msg = config['weeklyupdate']
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def mentions(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    if user_id in MENTIONTEAM:
        msg = config['mentions']
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def bunny(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    bunnylist=["/home/ubuntu/rabbitpic.jpg", "/home/ubuntu/rabbit1.jpg", "/home/ubuntu/rabbit2.jpg", "/home/ubuntu/rabbit3.jpg", "/home/ubuntu/rabbit4.jpg", "/home/ubuntu/rabbit5.jpg", "/home/ubuntu/rabbit6.jpg", "/home/ubuntu/rabbit7.jpg", "/home/ubuntu/rabbit8.jpg", "/home/ubuntu/rabbit9.jpg", "/home/ubuntu/rabbit10.jpg", "/home/ubuntu/rabbit11.jpg", "/home/ubuntu/rabbit12.jpg", "/home/ubuntu/rabbit13.jpg", "/home/ubuntu/rabbit14.jpg", "/home/ubuntu/rabbit15.jpg"]
    bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(bunnylist), "rb"))


###############################################################################

###### Error logging
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

###### Running the bot
def main():

# Create the EventHandler and pass it your bot's token
    print("Bot started")
    updater = Updater(bot_token,workers=10)

##### Get the dispatcher to register handlers
    dp = updater.dispatcher

##### CommandHandlers
    dp.add_handler(CommandHandler('id', getid))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("extras", extras))
    dp.add_handler(CommandHandler("community", community))
    dp.add_handler(CommandHandler("platforms", platforms))
    dp.add_handler(CommandHandler("heybot", heybot))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("conferences", conferences))
    dp.add_handler(CommandHandler("previousevents", previousevents))
    dp.add_handler(CommandHandler("videos", videos))
    dp.add_handler(CommandHandler("uraiden", uraiden))
    dp.add_handler(CommandHandler("whenmoon", whenmoon))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("tokenmodel", tokenmodel))
    dp.add_handler(CommandHandler("adminlist", adminlist))
    dp.add_handler(CommandHandler("ignorethat", ignorethat))
    dp.add_handler(CommandHandler("devcon", devcon))
    dp.add_handler(CommandHandler("adminpolicy", adminpolicy))
    dp.add_handler(CommandHandler("pulse", pulse))
    dp.add_handler(CommandHandler("nightly", nightly))
    dp.add_handler(CommandHandler("releases", releases))
    dp.add_handler(CommandHandler("email", email))
    dp.add_handler(CommandHandler("brainbot", brainbot))
    dp.add_handler(CommandHandler("RemindMeIn5Years", RemindMeIn5Years))
    dp.add_handler(CommandHandler("disclaimer", disclaimer))
    dp.add_handler(CommandHandler("rapps", rapps))
    dp.add_handler(CommandHandler("lefteris", lefteris))
    dp.add_handler(CommandHandler("weeklyupdate", weeklyupdate))
    dp.add_handler(CommandHandler("mentions", mentions))
    dp.add_handler(CommandHandler("bunny", bunny))
    dp.add_handler(CommandHandler("meme", meme))

##### MessageHandlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_member))
    dp.add_handler(MessageHandler(Filters.all, sameuser))


##### Log all errors
    dp.add_error_handler(error)

# Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
