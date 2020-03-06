from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, JobQueue
from telegram import ChatAction, ChatPermissions
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

if os.path.isfile("./config.yaml"):
    with open("./config.yaml") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
else:
    exit("No configuration file 'config.yaml' found")
    sys.exit()

##### Open fortune cookies
if os.path.isfile("./fortunes.json"):
    with open("./fortunes.json") as fortunes_file:
        fortunes = json.load(fortunes_file)
else:
    print("No fortune cookies file 'fortunes.json' found")

##### load config
bot_token            = config['bot_token']
bot                  = telegram.Bot(token=bot_token)

ADMINS               = config['ADMINS']
RNC                  = config['RNC_ID']
RNC_PLAYGROUND       = config['RNC_PLAYGROUND_ID']


##### global variables
PRIOR_WELCOME_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_WELCOME = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_CMD_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_CMD_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_USR_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_USR_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_SCRT_MSG_ID = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

##### FAQ IDs
FAQ                  = {
	RNC   : 0,
	RNC_PLAYGROUND   : 0
}

PRIOR_FAQ_MSG_ID = {
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

def delete(chat_id):
    try:
        bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
    except:
        pass
    try:
        bot.delete_message(chat_id=chat_id, message_id=PRIOR_CMD_MSG_ID[chat_id])
    except:
        pass

############################ Spam/Scam/Flood/Edit filter #######################

def spamfilter(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    text = update.message.text
    name = get_name(update.message.from_user)
    blacklist = config['blacklisted']
    msg_count = config['counts']['msg']
    spammerid = int
    moon_count = config['counts']['moon']
    botpoints =  config['counts']['botpoints']
    print(chat_id,user_id,moon_count,botpoints)
    triggers = config['triggers']
    config['previous_msg'] = text
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        previous_user = PRIOR_USR_ID[chat_id]
        config['previous_msg_id'] = message_id
    else:
        return

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
                context.bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

##### Flood filter
    if (user_id == previous_user) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        config['counts']['msg'] = msg_count + 1
        if (msg_count == 5):
	           update.message.reply_text("\xF0\x9F\x8C\x8A")
        if (msg_count >= 6):
            if spammerid != user_id:
                spammerid = user_id
                PRIOR_USR_ID[chat_id] = user_id
                bot.delete_message(chat_id=chat_id, message_id=message_id)
#                bot.restrictChatMember(chat_id,user_id = spammerid,can_send_messages=False,until_date=time.time()+int(float(60)*60)) # 60 min restriction
#                msg = ("Whoa there "+str(name)+"! You're typing at \xE2\x9A\xA1 speed! My flood filter has turned on to cool off that \xF0\x9F\x94\xA5 for an hour.")
                context.bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                pprint(spammerid)
                count = 0
    elif (user_id != previous_user) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        msg_count = 0
        config['counts']['msg'] = msg_count
        PRIOR_USR_ID[chat_id] = user_id

##### Prevent bot spam
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        config['counts']['moon'] = moon_count + 1

##### Edit message filter

def editfilter(update, context):
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
def forwardfilter(update, context):
    message_id = update.message.message_id
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
#    profile_pics = bot.getUserProfilePhotos(user_id=user_id)
    if PRIOR_WELCOME[chat_id] == 1 and user_id == PRIOR_USR_ID[chat_id]:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        pprint('forwarded photo')

############################### New Member #####################################

def new_chat_member(update, context):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    tag = update.message.from_user.username
    name = get_name(update.message.from_user)
    profile_pics = context.bot.getUserProfilePhotos(user_id=user_id)

##### Turn on welcome destruct timer
    if PRIOR_WELCOME[chat_id] == 0:
        PRIOR_WELCOME[chat_id] = 1
#### Welcome
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        bot.delete_message(chat_id=chat_id,message_id=message_id)
        pprint('New Member')
        if (len(tag) < 14):
            if tag != None:
                if (PRIOR_WELCOME_MSG_ID[chat_id] > 0 and profile_pics.total_count != 0):
                    context.bot.delete_message(chat_id=chat_id, message_id=PRIOR_WELCOME_MSG_ID[chat_id])
                    PRIOR_WELCOME[chat_id] = 0
                msg = ("Welcome @"+str(tag)+"! Check out our [Pinned Post](https://t.me/RaidenNetworkCommunity/2) and community [Discord](http://discord.raiden.community) for feeds on all things Raiden\xE2\x9A\xA1")
                message = context.bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                PRIOR_WELCOME_MSG_ID[chat_id] = int(message.message_id)
                job = context.job_queue.run_once(welcome_destruct, 300, context=(chat_id, user_id))
            elif profile_pics.total_count != 0:
                if PRIOR_WELCOME_MSG_ID[chat_id] > 0:
                    context.bot.delete_message(chat_id=chat_id, message_id=PRIOR_WELCOME_MSG_ID[chat_id])
                    PRIOR_WELCOME[chat_id] = 0
                msg = ("Welcome "+str(name)+"! Check out our [Pinned Post](https://t.me/RaidenNetworkCommunity/2) and community [Discord](http://discord.raiden.community) for feeds on all things Raiden\xE2\x9A\xA1")
                message = context.bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                PRIOR_WELCOME_MSG_ID[chat_id] = int(message.message_id)
                job = context.job_queue.run_once(welcome_destruct, 300, context=(chat_id, user_id))
        else:
            pprint('Long name')

################################ Commands ######################################

def getid(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    update.message.reply_text(str(update.message.from_user.first_name)+" : "+str(update.message.from_user.id))

def start(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    if (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        msg = config['pmme']
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
    else:
        msg = config['start']
        update.message.reply_text("Hey "+str(update.message.chat.first_name)+"! I'm a resource bot, message me here or in @RaidenNetworkCommunity telegram group.\n\nGet a list of my commands with /commands")

def commands(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['commands']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def extras(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    msg = config['extras']
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def community(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['community']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def platforms(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['platforms']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def heybot(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    msg = ("Hey "+str(update.message.from_user.first_name)+"! What's up?")
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def resources(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['resources']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def events(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['events']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def previousevents(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['previousevents']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def videos(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['videos']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def uraiden(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['uraiden']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def whenmoon(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['whenmoon']
    moon_count = config['counts']['moon']
    message_id = update.message.message_id
    name = get_name(update.message.from_user)
    if (moon_count >= 100) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        msg = ("We went "+str(moon_count)+" messages without asking when moon, good work team!")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['moon'] = 0
    elif (moon_count < 100) and (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        config['counts']['moon'] = moon_count + 1
        moon_count_remaining = 100 - moon_count
        msg = ("Sorry "+str(name)+"! When Moon only available every 100 messages. "+str(moon_count_remaining)+" to go!")
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rules(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['rules']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def tokenmodel(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['tokenmodel']
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminlist(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['adminlist']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def ignorethat(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    update.message.reply_text("I'm not sure I want to ignore that, "+str(update.message.from_user.first_name)+"...")

def devcon(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['devcon']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        elif PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def adminpolicy(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    message_id = update.message.message_id
    chat_id = update.message.chat.id
    if (update.message.chat.type == 'group') or (update.message.chat.type == 'supergroup'):
        msg = config['pmme']
        bot.sendMessage(chat_id=chat_id,text=msg,reply_to_message_id=message_id, parse_mode="Markdown",disable_web_page_preview=1)
    else:
        msg = config['adminpolicy']
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def pulse(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['pulse']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def nightly(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['nightly']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def releases(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['releases']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def email(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['email']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def brainbot(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['brainbot']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def RemindMeIn5Years(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    update.message.reply_text("Setting a reminder for "+str(update.message.from_user.first_name)+" 5 years from now.")

def disclaimer(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['disclaimer']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def rapps(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['rapps']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def faucets(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['faucets']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def lefteris(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    lefterislist=["/home/ubuntu/lefteris.jpg", "/home/ubuntu/lefteris2.jpg"]
    bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(lefterislist), "rb"))

def meme(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    memelist=["/home/ubuntu/meme.mp4", "/home/ubuntu/meme3.mp4", "/home/ubuntu/meme6.mp4", "/home/ubuntu/meme7.mp4", "/home/ubuntu/meme8.mp4"]
    bot.sendVideo(chat_id=chat_id,timeout=13, video=open(random.choice(memelist), "rb"))

def weeklyupdate(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    msg = config['weeklyupdate']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def mentions(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    msg = config['mentions']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def bunny(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    bunnylist=["/home/ubuntu/rabbitpic.jpg", "/home/ubuntu/rabbit1.jpg", "/home/ubuntu/rabbit2.jpg", "/home/ubuntu/rabbit3.jpg", "/home/ubuntu/rabbit4.jpg", "/home/ubuntu/rabbit5.jpg", "/home/ubuntu/rabbit6.jpg", "/home/ubuntu/rabbit7.jpg", "/home/ubuntu/rabbit8.jpg", "/home/ubuntu/rabbit9.jpg", "/home/ubuntu/rabbit10.jpg", "/home/ubuntu/rabbit11.jpg", "/home/ubuntu/rabbit12.jpg", "/home/ubuntu/rabbit13.jpg", "/home/ubuntu/rabbit14.jpg", "/home/ubuntu/rabbit15.jpg", "/home/ubuntu/rabbit16.jpg", "/home/ubuntu/rabbit17.jpg", "/home/ubuntu/rabbit18.jpg", "/home/ubuntu/rabbit19.jpg"]
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(bunnylist), "rb"))
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendPhoto(chat_id=chat_id, photo=open(random.choice(bunnylist), "rb"))


def fistbump(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = '\xF0\x9F\x91\x8A'
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def doublefistbump(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = '\xF0\x9F\x91\x8A \xF0\x9F\x91\x8A'
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            remove(update, context)
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_ID[chat_id] = int(message_id)
    else:
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

def fortune(update, context):
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

def communityfaq(update, context):

    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['communityfaq']
    message_id = update.message.message_id
#    user_id = update.message.from_user.id if removed by someone other than the person using the FAQ might need to make it user specific
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if PRIOR_CMD_MSG_ID[chat_id] > 0:
            delete(chat_id)
            try:
                bot.delete_message(chat_id=chat_id,message_id=PRIOR_FAQ_MSG_ID[chat_id])
            except:
                print("Starting FAQ")
                FAQ[chat_id] = True
        message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        PRIOR_FAQ_MSG_ID[chat_id] = int(message.message_id)
        PRIOR_CMD_MSG_ID[chat_id] = PRIOR_FAQ_MSG_ID[chat_id]
        PRIOR_CMD_ID[chat_id] = int(message_id)
        FAQ[chat_id] = True
    else:
        bot.delete_message(chat_id=chat_id,message_id=message_id)

def mainnet(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['mainnet']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def testnet(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['testnet']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def standardization(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['standardization']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def plasma(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['plasma']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def channels(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['channels']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def monitoring(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['monitoring']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def pathfinding(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['pathfinding']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def cost(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['cost']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def speed(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['speed']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def privacy(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['privacy']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def future(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['future']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def developers(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['developers']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def obsolete(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['obsolete']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def token(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['token']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def CommunityFAQdisclaimer(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['CommunityFAQdisclaimer']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)


def everything(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['everything']
    message_id = update.message.message_id
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if FAQ[chat_id] == True:
            if PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]:
                delete(chat_id)
            message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
            PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
            PRIOR_CMD_ID[chat_id] = int(message_id)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def back(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND) and (PRIOR_CMD_MSG_ID[chat_id] != PRIOR_FAQ_MSG_ID[chat_id]):
            delete(chat_id)
            bot.delete_message(chat_id=chat_id,message_id=message_id)
            communityfaq(update, context)
        else:
            bot.delete_message(chat_id=chat_id,message_id=message_id)

def remove(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat.id
    msg = config['remove']
    message_id = update.message.message_id
    if FAQ[chat_id] == True:
        if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
            delete(chat_id)
            try:
                bot.delete_message(chat_id=chat_id, message_id=PRIOR_FAQ_MSG_ID[chat_id])
            except:
                print("FAQ post already removed")
            finally:
                message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                PRIOR_CMD_MSG_ID[chat_id] = 0
                PRIOR_CMD_ID[chat_id] = int(message_id)
                PRIOR_FAQ_MSG_ID[chat_id] = 0
                FAQ[chat_id] = False
                print("Ending FAQ")
        else:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
#    else:   ###maybe make remove function work anytime
#        if ((chat_id == RNC or chat_id == RNC_PLAYGROUND) and PRIOR_CMD_MSG_ID[chat_id] > 0):
#            delete(chat_id)

###################################### Secret ##################################

###### send self destruct message
def self_destruct(context):
    chat_id = context.job.context[0]
    user_id = context.job.context[1]
    message = bot.send_message(chat_id, text='Message self destructing.')
    bot.delete_message(chat_id,message_id=message.message_id)
    try:
        bot.delete_message(chat_id,message_id=PRIOR_CMD_MSG_ID[chat_id])
        bot.delete_message(chat_id,message_id=PRIOR_SCRT_MSG_ID[chat_id])
        message = bot.send_message(chat_id, text='Message self destructed.')
    except:
        print("Message already deleted.")
    PRIOR_SCRT_MSG_ID[chat_id] = 0
    print("Message self destruct success")

def welcome_destruct(context):
    chat_id = context.job.context[0]
    user_id = context.job.context[1]
    if PRIOR_WELCOME[chat_id] != 0:
        bot.delete_message(chat_id,message_id=PRIOR_WELCOME_MSG_ID[chat_id])
        PRIOR_WELCOME[chat_id] = 0
        PRIOR_WELCOME_MSG_ID[chat_id] = 0
        print("Welcome destruct success")

###### register self destruct command and arg
def secret(update, context, args):
    pprint(update.message.chat.__dict__, indent=4)
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    user_id = update.message.from_user.id
#    config['previous_msg'] = text
    name = get_name(update.message.from_user)
    if (chat_id == RNC or chat_id == RNC_PLAYGROUND):
        if (PRIOR_USR_ID[chat_id] == user_id and PRIOR_SCRT_MSG_ID[chat_id] == 0):
            secret_id = config['previous_msg_id']
            try:
                # args[0] should contain the time for the timer in minutes
                due = int(args[0])*60
                if due == 60:
                    msg = (str(name)+" set a message self destruct for 1 minute.")
                else:
                    msg = (str(name)+" set a message self destruct for "+str(due / 60)+" minutes.")
                if due < 0:
                    update.message.reply_text('Sorry we can not go back to the future!')
                    return
                elif due > 600:
                    update.message.reply_text('Too Long. Max value: 10')
                    return
                else:
                    # Add job to queue
                    message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)

                    PRIOR_SCRT_MSG_ID[chat_id] = int(secret_id)
                    PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
                    PRIOR_CMD_ID[chat_id] = int(message_id)
                    job = context.job_queue.run_once(self_destruct, due, context=chat_id)
                    try:
                        bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
                    except:
                        print("Message already deleted.")
            except (IndexError, ValueError):
                print("Error in value. Self destruct set to default.")
                msg = ("No value specified. Message self destruct of 1 minute set.")
                message = bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
                PRIOR_SCRT_MSG_ID[chat_id] = int(secret_id)
                PRIOR_CMD_MSG_ID[chat_id] = int(message.message_id)
                PRIOR_CMD_ID[chat_id] = int(message_id)
                job = context.job_queue.run_once(self_destruct, 60, context=chat_id)
                try:
                    bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
                except:
                    print("Message already deleted.")
        else:
            print("Secret failed. Not in RNC or not same user")
            try:
                context.bot.delete_message(chat_id=chat_id,message_id=PRIOR_CMD_ID[chat_id])
            except:
                print("Message already deleted.")


############################### Bot points functions ###########################
def goodbot(update, context):
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

def badbot(update, context):
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

def botpoints(update, context):
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
def prev_moon(update, context):
    pprint(update.message.chat.__dict__, indent=4)
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    if user_id in ADMINS:
        value = config['previous_msg']
        msg = ("Time since moon is now "+str(value))
        bot.sendMessage(chat_id=chat_id,text=msg,parse_mode="Markdown",disable_web_page_preview=1)
        config['counts']['moon'] = int(value)

def prev_botpoints(update, context):
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
def error(update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

###### Running the bot
def main():
    print("Bot started")

##### Create the EventHandler and pass it your bot's token
    updater = Updater(bot_token, use_context=True)

##### Get the dispatcher to register handlers
    dp = updater.dispatcher

##### CommandHandlers
    dp.add_handler(CommandHandler("getid", getid))
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
    dp.add_handler(CommandHandler("faucets", faucets))
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
    dp.add_handler(CommandHandler("token", token))
    dp.add_handler(CommandHandler("CommunityFAQdisclaimer", CommunityFAQdisclaimer))
    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("remove", remove))

##### Secret and self destruct
    dp.add_handler(CommandHandler("secret", secret, pass_args=True, pass_job_queue=True))

##### Bot points functions
    dp.add_handler(CommandHandler("goodbot", goodbot))
    dp.add_handler(CommandHandler("badbot", badbot))
    dp.add_handler(CommandHandler("botpoints", botpoints))

##### Misc functions
    dp.add_handler(CommandHandler("prev_moon", prev_moon))
    dp.add_handler(CommandHandler("prev_botpoints", prev_botpoints))

##### MessageHandlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_chat_member, pass_job_queue=True))
    dp.add_handler(MessageHandler((Filters.forwarded & Filters.photo), forwardfilter))
    dp.add_handler(MessageHandler(Filters.update.edited_message, editfilter))
    dp.add_handler(MessageHandler(Filters.forwarded, forwardfilter))
    dp.add_handler(MessageHandler(Filters.text & (~ (Filters.forwarded | Filters.update.edited_message)), spamfilter))


##### Error handler
    dp.add_error_handler(error)

##### Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
