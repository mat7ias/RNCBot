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

###### To add your own follow the template of (for examples look below):
###### def COMMAND(bot, update):
###### update.message.reply_text("ADD TEXT HERE",disable_web_page_preview=1)
###### Then make sure you add the commands in the CommandHandler section:
###### dp.add_handler(CommandHandler("COMMAND", command))
###### You got this!

def commands(bot, update):
    update.message.reply_text("In RaidenCommunityBot commands:\n\n"
        "/resources\n"
        "/videos\n"
        "/events\n"
        "/rules\n"
        "/adminlist")

def heybot(bot, update):
    update.message.reply_text('Hey!')

def resources(bot, update):
    update.message.reply_text('Raiden Network resources:\n\n'
        "Website raiden.network/\n"
        "FAQ raiden.network/faq.html\n"
        "Github github.com/raiden-network/raiden\n"
        "Documentation readthedocs.org/projects/raiden-network/\n"
        "Specification PDF media.readthedocs.org/pdf/raiden-network-specificati"
        "on/latest/raiden-network-specification.pdf\n"
        "Medium Publications medium.com/@raiden_network\n"
        "Weekly Github Update reddit.com/user/bor4/posts/\n\n"
        "MicroRaiden:\n\n"
        "uRaiden site: micro.raiden.network/\n"
        "uRaiden codebase: github.com/raiden-network/microraiden\n"
        "uRaiden docs: microraiden.readthedocs.io/en/docs-develop/\n"
        "uRaiden dev chat: gitter.im/raiden-network/microraiden\n"
        "uRaiden testnet demos: demo.micro.raiden.network/\n\n"
        "Feel free to PM me @RaidenCommunityInfoBot",disable_web_page_preview=1)

def events(bot, update):
    update.message.reply_text("Upcoming Events:\n\n"
        "Recent Events:\n"
        "5/9 - Full Node: Mass adApption & use-cases https://www.eventbrite.com"
        "/e/mass-adapption-use-cases-golem-raiden-status-tickets-49559434603\n"
        "7/9-9/9 - ETHBerlin Scaling & Interoperability Panel ethberlin.com/\n"
        "28/8 - Copenhagen Ethereum Meetup twitter.com/raiden_network/status/10"
        "30051960949551109\n"
        "19/7-20/7 - DappCon Lefteris and Augusto dappcon.io/#speakers",
        disable_web_page_preview=1)

def videos(bot, update):
    update.message.reply_text("Raiden Network videos/presentations:\n"
        "Raiden youtube channel youtube.com/channel/UCoUP_hnjUddEvbxmtNCcApg\n"
        "Brainbot Technologies channel youtube.com/channel/UCAfSoSy9FK5UqlSxqcs"
        "QElA/videos\n"
        "Lefteris Raiden presentation youtu.be/93qOwUSj4PQ\n"
        "Lefteris interview devcon3 youtu.be/00RPE96LRVM\n"
        "The Raiden Network Heiko Hees devcon2 youtu.be/4igFqFqQga4\n"
        "Edcon 2018 youtu.be/VsZuDJMmVPY?t=7h45m51s\n"
        "Augusto explains Raiden oktahedron.diskordia.org/?podcast=oh007-raiden"
        "#t=1:56.687\n"
        "On The L2 Summit State Channel Panel youtu.be/jzoS0tPUAiQ?t=2h10m9s\n"
        "Off The Chain presentation youtu.be/8Duil4pLzhI\n"
        "DAPPCON 2018 youtu.be/hSMIpl6e_Ow\n"
        "DAPPCON 2018 Panel Talking State Channels and Plasma youtu.be/zmS0i3ZQ"
        "Zak\n"
        "Copenhagen Ethereum Meetup Jacob youtu.be/arecj2vyjlE\n"
        "Tackling Scalability Panel youtu.be/AH2g-KpPk7w\n"
        "Mass Adoption and Use-Cases youtu.be/GrWqRVDOC4M\n"
        "ETHBerlin view.ly/v/MrLm3vSB1XEK\n\n"
        "uRaiden videos:\n"
        "uRaiden presentation Devcon3: youtu.be/yx0__aFvjzk?t=9m35s\n"
        "uRaiden Berlin Meetup drone demo: youtube.com/watch?v=E6CIgJPxgpQ\n"
        "ScalingNOW! Loredana talk: youtu.be/81gK-5qLFeg\n\n"
        "Feel free to PM me @RaidenCommunityInfoBot"
        ,disable_web_page_preview=1)

def whenmoon(bot, update):
    update.message.reply_text("The speed of light is 299.8km/s (or 299.792.458"
        "m/s). Average distance to moon is 384400km at the closest two points. "
        "1.28 seconds on average for information travelling at the speed of"
        "light to reach the Moon.\n"
        "Although I think we can be more accurate about When Moon since the "
        "distance fluctuates between 363104-405704km. Which means that if we "
        "ignore computation/processing time the shortest time to moon is 1.21 "
        "seconds (time for light to reach surface of the Moon from the Earth:"
        "https://i.imgur.com/nj8q3db.png).\n"
        "For the longest time we need to do a bit more and make some "
        "assumptions. First is that being the longest distance also implied "
        "that we have no direct line of sight and that we will need to send "
        "our Raiden Network transfer with the help of either satellites."
        "OneWeb are setting up satellites with a low earth orbit of 1200km "
        "(https://en.wikipedia.org/wiki/OneWeb_satellite_constellation) so "
        "let's assume that's our satellite orbit for the Earth.\n"
        "For the Moon we will also need to send the Raiden Network transfer to "
        "the furthest point and again need to use satellites. The lowest "
        "realistic lunar orbit is 15km (to avoid hitting lunar mountains, "
        "which reach heights of 6.1km; "
        "https://en.wikipedia.org/wiki/Lunar_orbit). \n"
        "So now we need to find the distance for this path: "
        "https://i.imgur.com/a8VxSnm.png"
        "With some quick maths we can figure this distance out as such "
        "https://i.imgur.com/1zNeIMt.png and our final maximum distance being "
        "a total of 431538km. Again if we ignore computation/processing time "
        "between the Payee and Payer then we have a maximum transfer time of "
        "1.44 seconds.\n"
        "I am happy to officially announce that Raiden Network will Moon in "
        "1.21-1.44 seconds once the milestone is reached in Q4 2018."
        "Hope this helps!",disable_web_page_preview=1)

def rules(bot, update):
    update.message.reply_text("1) This channel is about freedom of speech, "
        "but please keep in mind that it has its limits. Passionate debate is "
        "welcome, but unreasonable disrespect to any fellow members of the "
        "group (and especially the Raiden team) will not be tolerated. Doing "
        "so may result in your message being removed (this will be discussed "
        "with you in private messages).\n"
        "2) Not allowed: referral links unrelated to Raiden, telegram channel "
        "links, self promo media, pump and dump groups, NSFW content,  "
        "excessive swearing, spam in general, doxxing.\n"
        "3) Excessive trolling will result in removed messages.\n"
        "4) Please stay on topic, this channel is about the Raiden Network "
        "and scaling.")

def adminlist(bot, update):
    update.message.reply_text("RNC Admin List:\n\n"
        "Mattias - @Mat7ias\n"
        "Boris - @BOR44\n"
        "Emil - @emiliorull\n"
        "Chomsky - @Chomsky12\n"
        "Ryan - @R2theD2\n"
        "Tim - @Kaleaso\n"
        "Hudazara - @Hudazara\n")

def ignorethat(bot, update):
    update.message.reply_text("I'm not sure I want to ignore that...")

###############################################################################

###### Error logging
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

###### Running the bot
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_token)

##### Get the dispatcher to register handlers
    dp = updater.dispatcher

##### CommandHandlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("heybot", heybot))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("events", events))
    dp.add_handler(CommandHandler("videos", videos))
    dp.add_handler(CommandHandler("whenmoon", whenmoon))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("adminlist", adminlist))
    dp.add_handler(CommandHandler("ignorethat", ignorethat))

##### MessageHandlers
    dp.add_handler(MessageHandler(Filters.all, sameuser))

##### Log all errors
    dp.add_error_handler(error)

# Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
