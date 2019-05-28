from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time
import os
import string
from pprint import pprint
import sys
import yaml
import telegram
import random
import json


##### Configure Logging

FORMAT = '%(asctime)s -- %(levelname)s -- %(module)s %(lineno)d -- %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger('root')
logger.info("Running "+sys.argv[0])

##### Open config_file

if os.path.isfile("bot/RaidenBot/config.yaml"):
    with open("bot/RaidenBot/config.yaml") as config_file:
        config = yaml.load(config_file)
else:
    exit("No configuration file 'config.yaml' found")
    sys.exit()


if os.path.isfile("bot/RaidenBot/fortunes.json"):
    with open("bot/RaidenBot/fortunes.json") as fortunes_file:
        fortunes = json.load(fortunes_file)
else:
    print("No fortune cookies file 'fortunes.json' found")

##### load config
bot_token      = config['bot_token']
bot            = telegram.Bot(token=bot_token)

ADMINS               = config['ADMINS']
MENTIONTEAM          = config['MENTIONTEAM']
RNC                  = config['RNC_ID']
RNC_PLAYGROUND       = config['RNC_PLAYGROUND_ID']

FAQ                  = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_WELCOME_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_CMD_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_FAQ_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_CMD_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}



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

############################ Spam/Scam/Flood/Edit filter #######################

def spamfilter(bot, update):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    previous_user = config['previous']['user_id']
    blacklist = config['blacklisted']
    text = update.message.text
    msg_count = config['counts']['msg']
    spammerid = int
    name = get_name(update.message.from_user)
    chat_id = update.message.chat.id
    config['previous_msg'] = text
    moon_count = config['counts']['moon']
    botpoints =  config['counts']['botpoints']
    print(chat_id,user_id,moon_count,botpoints)
    triggers = config['triggers']

    if text != None:

##### Blacklist filter
        for x in blacklist:
            if x in text:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
                bot.restrict_chat_member(chat_id=chat_id,user_id=user_id,can_send_messages=False,can_send_media_messages=False,can_send_other_messages=False,can_add_web_page_previews=False)
                pprint('blacklisted word')

##### Scam Triggers
        for y in triggers:
            if y in text:
                badword = y
                msg = ("#No"+str(badword)+", watch out for scams!")
                bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

##### Flood filter
    if (user_id == previous_user) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        config['counts']['msg'] = msg_count + 1
        if (msg_count == 5):
	           update.message.reply_text("\xF0\x9F\x8C\x8A")
        if (msg_count >= 6):
            if spammerid != user_id:
                spammerid = user_id
                bot.delete_message(chat_id=chat_id, message_id=message_id)
                bot.restrictChatMember(chat_id,user_id = spammerid,can_send_messages=False,until_date=time.time()+int(float(60)*60)) # 60 min restriction
                msg = ("Whoa there "+str(name)+"! You're typing at \xE2\x9A\xA1 speed! My flood filter has turned on to cool off that \xF0\x9F\x94\xA5 for an hour.")
                bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                pprint(spammerid)
                count = 0
    elif (user_id != previous_user) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        msg_count = 0
        config['counts']['msg'] = msg_count
        config['previous']['user_id'] = user_id

##### Prevent bot spam
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        config['counts']['moon'] = moon_count + 1

##### Edit message filter

def editfilter(bot, update):
    text = update.edited_message.text
    message_id = update.edited_message.message_id
    chat_id = update.edited_message.chat.id
    blacklist = config['blacklisted']
    if text != None:
        for x in blacklist:
            if x in text:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
                pprint('blacklisted edited word')

##### Forwarded photo filter
def forwardfilter(bot, update):
    message_id = update.message.message_id
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    profile_pics = bot.getUserProfilePhotos(user_id=user_id)
    if profile_pics.total_count == 0:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        pprint('forwarded photo')

############################### New Member #####################################

def new_chat_member(bot, update):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    tag = update.message.from_user.username
    name = get_name(update.message.from_user)
    profile_pics = bot.getUserProfilePhotos(user_id=user_id)
    if update.message.chat.type == 'supergroup':
        bot.delete_message(chat_id=chat_id,message_id=message_id)
        if (profile_pics.total_count == 0 or tag == None):
            bot.restrict_chat_member(chat_id=chat_id,user_id=user_id,until_date=(time.time()+int(float(6000)*6000)),can_send_messages=True,can_send_media_messages=False,can_send_other_messages=False,can_add_web_page_previews=False)
            pprint('New Member. No profile pic or tag')
        else:
            bot.restrict_chat_member(chat_id=chat_id,user_id=user_id,until_date=(time.time()+int(float(6000)*6000)),can_send_messages=True,can_send_media_messages=True,can_send_other_messages=False,can_add_web_page_previews=False)
            pprint('New Member')
        if (len(name) < 21):
            if tag != None:
                if PRIOR_WELCOME_MSG_ID[chat_id] > 0:
                    bot.delete_message(chat_id=chat_id, message_id=PRIOR_WELCOME_MSG_ID[chat_id])
                msg = ("Welcome @"+str(tag)+"! Check out our [Pinned Post](https://t.me/RaidenNetworkCommunity/2) and community [Discord](https://discord.gg/zZjYJ6e) for feeds on all things Raiden\xE2\x9A\xA1")
                message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                PRIOR_WELCOME_MSG_ID[chat_id] = int(message.message_id)
            elif profile_pics.total_count != 0:
                if PRIOR_WELCOME_MSG_ID[chat_id] > 0:
                    bot.delete_message(chat_id=chat_id, message_id=PRIOR_WELCOME_MSG_ID[chat_id])
                msg = ("Welcome "+str(name)+"! Check out our [Pinned Post](https://t.me/RaidenNetworkCommunity/2) and community [Discord](https://discord.gg/zZjYJ6e) for feeds on all things Raiden\xE2\x9A\xA1")
                message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                PRIOR_WELCOME_MSG_ID[chat_id] = int(message.message_id)
        else:
            pprint('Long name')

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
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
    else:
        msg = config['start']
        update.message.reply_text("Hey "+str(update.message.chat.first_name)+"! I'm a resource bot, message me here or in @RaidenNetworkCommunity telegram group.\n\nGet a list of my commands with /commands")

def commands(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['commands']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def extras(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    msg = config['extras']
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def community(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['community']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def platforms(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['platforms']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def heybot(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    msg = ("Hey "+str(update.message.from_user.first_name)+"! What's up?")
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def resources(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['resources']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def events(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['events']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def previousevents(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['previousevents']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def videos(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['videos']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def uraiden(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['uraiden']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def whenmoon(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['whenmoon']
    moon_count = config['counts']['moon']
    message_id = update.message.message_id
    if (moon_count >= 100) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        msg = ("We went "+str(moon_count)+" messages without asking when moon, good work team!")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['moon'] = 0
    if (moon_count < 100) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        config['counts']['moon'] = moon_count + 1
        moon_count_remaining = 100 - moon_count
        msg = ("When Moon only available every 100 messages. "+str(moon_count_remaining)+" to go!")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
    elif (chat_id != RNC and chat_id != RNC_PLAYGROUND):
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rules(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['rules']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def tokenmodel(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['tokenmodel']
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminlist(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['adminlist']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def ignorethat(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    update.message.reply_text("I'm not sure I want to ignore that, "+str(update.message.from_user.first_name)+"...")

def devcon(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['devcon']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
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
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def nightly(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['nightly']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def releases(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['releases']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def email(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['email']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def brainbot(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['brainbot']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def RemindMeIn5Years(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    update.message.reply_text("Setting a reminder for "+str(update.message.from_user.first_name)+" 5 years from now.")

def disclaimer(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['disclaimer']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rapps(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['rapps']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
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
    msg = config['weeklyupdate']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
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
    message_id = update.message.message_id
    bunnylist=["/home/ubuntu/rabbitpic.jpg", "/home/ubuntu/rabbit1.jpg", "/home/ubuntu/rabbit2.jpg", "/home/ubuntu/rabbit3.jpg", "/home/ubuntu/rabbit4.jpg", "/home/ubuntu/rabbit5.jpg", "/home/ubuntu/rabbit6.jpg", "/home/ubuntu/rabbit7.jpg", "/home/ubuntu/rabbit8.jpg", "/home/ubuntu/rabbit9.jpg", "/home/ubuntu/rabbit10.jpg", "/home/ubuntu/rabbit11.jpg", "/home/ubuntu/rabbit12.jpg", "/home/ubuntu/rabbit13.jpg", "/home/ubuntu/rabbit14.jpg", "/home/ubuntu/rabbit15.jpg", "/home/ubuntu/rabbit16.jpg", "/home/ubuntu/rabbit17.jpg", "/home/ubuntu/rabbit18.jpg", "/home/ubuntu/rabbit19.jpg"]
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(bunnylist), "rb"))
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(bunnylist), "rb"))


def fistbump(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = '\xF0\x9F\x91\x8A'
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def doublefistbump(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = '\xF0\x9F\x91\x8A \xF0\x9F\x91\x8A'
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(bot, update)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def fortune(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    previous_fortune_id = config['previous']['fortune']
    if (previous_fortune_id == user_id + 1) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        message_id = update.message.message_id
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    elif (user_id == previous_fortune_id) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        msg = ("One who asks for many fortunes in a row, is one who should rethink their life.")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['previous']['fortune'] = user_id + 1
    elif (user_id != previous_fortune_id) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        msg = random.choice(fortunes)
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['previous']['fortune'] = user_id
    else:
        msg = random.choice(fortunes)
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)


############################### FAQ functions ##################################

def communityfaq(bot, update):

    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['communityfaq']
    message_id = update.message.message_id
#    user_id = update.message.from_user.id if removed by someone other than the person using the FAQ might need to make it user specific
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if PRIOR_CMD_MSG_ID[chat_id] == 1:
            bot.delete_message(chat_id=chat_id,message_id=message_id)
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_FAQ_MSG_ID[chat_id])
        elif (PRIOR_CMD_MSG_ID[chat_id] > 1 and PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]):
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_FAQ_MSG_ID[chat_id])
        elif PRIOR_CMD_MSG_ID[chat_id] > 1 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_FAQ_MSG_ID[chat_id])
        elif PRIOR_CMD_MSG_ID[chat_id] > 1:
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_FAQ_MSG_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_FAQ_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_MSG_ID[chat_id] = PRIOR_FAQ_MSG_ID[chat_id]
        PRIOR_CMD_ID[chat_id] = int(message_id)
        if FAQ[chat_id] != True:
            FAQ[chat_id] = True
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def mainnet(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['mainnet']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def testnet(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['testnet']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def standardization(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['standardization']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def plasma(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['plasma']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def channels(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['channels']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def monitoring(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['monitoring']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def pathfinding(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['pathfinding']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def cost(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['cost']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def speed(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['speed']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def privacy(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['privacy']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def future(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['future']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def developers(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['developers']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def obsolete(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['obsolete']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)


def everything(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['everything']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and (PRIOR_FAQ_MSG_ID[chat_id] != 0 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id])):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def back(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if (PRIOR_CMD_MSG_ID[chat_id] > 1 and PRIOR_FAQ_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]):
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            elif PRIOR_CMD_MSG_ID[chat_id] > 1:
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=message_id)
            PRIOR_CMD_MSG_ID[chat_id] = PRIOR_FAQ_MSG_ID[chat_id]
            PRIOR_CMD_ID[chat_id] = 1
        else:
            bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)


def remove(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['remove']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            if PRIOR_CMD_MSG_ID[chat_id] == 1:
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_ID[chat_id])
            elif (PRIOR_CMD_MSG_ID[chat_id] > 1 and PRIOR_CMD_MSG_ID[chat_id] == PRIOR_FAQ_MSG_ID[chat_id]):
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_FAQ_MSG_ID[chat_id])

            elif (PRIOR_CMD_MSG_ID[chat_id] > 1 and PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]):

                bot.delete_message(chat_id=chat_id, message_id=PRIOR_FAQ_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            elif PRIOR_CMD_MSG_ID[chat_id] > 1:
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_FAQ_MSG_ID[chat_id])
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])

            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = 0
            PRIOR_CMD_ID[chat_id] = int(message_id)
            PRIOR_FAQ_MSG_ID[chat_id] = 0
            FAQ[chat_id] = False
    else:
        bot.delete_message(chat_id=chat_id, message_id=message_id)


############################### Bot points functions ###########################
def goodbot(bot, update):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    botpoints = config['counts']['botpoints']
    previous_botpoints_id = config['previous']['botpoints_id']
    if (previous_botpoints_id == user_id + 1) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        message_id = update.message.message_id
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    elif (user_id == previous_botpoints_id) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        msg = ("Only one point at a time.")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['previous']['botpoints_id'] = user_id + 1
    elif (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        botpoints = config['counts']['botpoints'] + 1
        msg = (str(random.choice(config['goodbot']))+" "+str(botpoints))
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['botpoints'] = botpoints
        config['previous']['botpoints_id'] = user_id

def badbot(bot, update):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    botpoints = config['counts']['botpoints']
    previous_botpoints_id = config['previous']['botpoints_id']
    if (previous_botpoints_id == user_id + 1) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        message_id = update.message.message_id
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    elif (user_id == previous_botpoints_id) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        msg = ("Only one point at a time.")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['previous']['botpoints_id'] = user_id + 1
    elif (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        botpoints = config['counts']['botpoints'] - 1
        msg = (str(random.choice(config['badbot']))+" "+str(botpoints))
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['botpoints'] = botpoints

def botpoints(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    message_id = update.message.message_id
    value = config['counts']['botpoints']
    msg = ("Current bot points at "+str(value))
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
            bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

############################### Misc functions #################################
###### Edit time to moon/points
def prev_moon(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    if user_id in ADMINS:
        value = config['previous_msg']
        msg = ("Time since moon is now "+str(value))
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['moon'] = int(value)

def prev_botpoints(bot, update):
    pprint(update.message.chat.__dict__, indent=4)
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    if user_id in ADMINS:
        value = config['previous_msg']
        msg = ("Botpoints now "+str(value))
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['botpoints'] = int(value)



###############################################################################

###### Error logging
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

###### Running the bot
def main():
    print("Bot started")

##### Create the EventHandler and pass it your bot's token
    updater = Updater(bot_token,workers=10)

##### Get the dispatcher to register handlers
    dp = updater.dispatcher

##### CommandHandlers
    dp.add_handler(CommandHandler('getid', getid))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("extras", extras))
    dp.add_handler(CommandHandler("community", community))
    dp.add_handler(CommandHandler("platforms", platforms))
    dp.add_handler(CommandHandler("heybot", heybot))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("events", events))
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
    dp.add_handler(CommandHandler("fistbump", fistbump))
    dp.add_handler(CommandHandler("doublefistbump", doublefistbump))
    dp.add_handler(CommandHandler("fortune", fortune))

##### Community FAQ functions
    dp.add_handler(CommandHandler("communityfaq", communityfaq))
    dp.add_handler(CommandHandler("mainnet", mainnet))
    dp.add_handler(CommandHandler("testnet", testnet))
    dp.add_handler(CommandHandler("standardization", standardization))
    dp.add_handler(CommandHandler("plasma", plasma))
    dp.add_handler(CommandHandler("channels", channels))
    dp.add_handler(CommandHandler("monitoring", monitoring))
    dp.add_handler(CommandHandler("pathfinding", pathfinding))
    dp.add_handler(CommandHandler("cost", cost))
    dp.add_handler(CommandHandler("speed", speed))
    dp.add_handler(CommandHandler("privacy", privacy))
    dp.add_handler(CommandHandler("future", future))
    dp.add_handler(CommandHandler("developers", developers))
    dp.add_handler(CommandHandler("obsolete", obsolete))
    dp.add_handler(CommandHandler("everything", everything))
    dp.add_handler(CommandHandler("additional", community))


    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("remove", remove))


##### Bot points functions
    dp.add_handler(CommandHandler("goodbot", goodbot))
    dp.add_handler(CommandHandler("badbot", badbot))
    dp.add_handler(CommandHandler("botpoints", botpoints))

##### Misc functions
    dp.add_handler(CommandHandler("prev_moon", prev_moon))
    dp.add_handler(CommandHandler("prev_botpoints", prev_botpoints))



##### MessageHandlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_member))
    dp.add_handler(MessageHandler((Filters.forwarded & Filters.photo), forwardfilter))
    dp.add_handler(MessageHandler(Filters.all, spamfilter,edited_updates=False))
    dp.add_handler(MessageHandler(Filters.all, editfilter,edited_updates=True))

##### Error handler
    dp.add_error_handler(error)

##### Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
