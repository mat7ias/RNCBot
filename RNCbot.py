from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


###### Commands
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def resources(bot, update):
    update.message.reply_text('Raiden Network resources:\n\n'
        "Website raiden.network/\n"
	    "FAQ raiden.network/faq.html\n"
	    "Github github.com/raiden-network/raiden\n"
	    "Documentation readthedocs.org/projects/raiden-network/\n"
	    "Specification PDF media.readthedocs.org/pdf/raiden-network-specification/latest/raiden-network-specification.pdf\n"
	    "Medium Publications medium.com/@raiden_network\n"
	    "Weekly Github Update reddit.com/user/bor4/posts/\n\n"

	    "Feel free to PM me @RaidenCommunityInfoBot",disable_web_page_preview=1)

def events(bot, update):
    update.message.reply_text("Upcoming Events:\n\n"
        "Recent Events:\n"
        "5/9 - Full Node: Mass adApption & use-cases https://www.eventbrite.com/e/mass-adapption-use-cases-golem-raiden-status-tickets-49559434603\n"
        "7/9-9/9 - ETHBerlin Scaling & Interoperability Panel ethberlin.com/\n"
        "28/8 - Copenhagen Ethereum Meetup twitter.com/raiden_network/status/1030051960949551109\n"
        "19/7-20/7 - DappCon Lefteris and Augusto dappcon.io/#speakers",disable_web_page_preview=1)

def videos(bot, update):
    update.message.reply_text("Raiden Network videos/presentations:\n"
        "Raiden youtube channel youtube.com/channel/UCoUP_hnjUddEvbxmtNCcApg\n"
        "Brainbot Technologies channel youtube.com/channel/UCAfSoSy9FK5UqlSxqcsQElA/videos\n"
        "Lefteris Raiden presentation youtu.be/93qOwUSj4PQ\n"
        "Lefteris interview devcon3 youtu.be/00RPE96LRVM\n"
        "The Raiden Network Heiko Hees devcon2 youtu.be/4igFqFqQga4\n"
        "Edcon 2018 youtu.be/VsZuDJMmVPY?t=7h45m51s\n"
        "Augusto explains Raiden oktahedron.diskordia.org/?podcast=oh007-raiden#t=1:56.687\n"
        "On The L2 Summit State Channel Panel youtu.be/jzoS0tPUAiQ?t=2h10m9s\n"
        "Off The Chain presentation youtu.be/8Duil4pLzhI\n"
        "DAPPCON 2018 youtu.be/hSMIpl6e_Ow\n"
        "DAPPCON 2018 Panel Talking State Channels and Plasma youtu.be/zmS0i3ZQZak\n"
        "Copenhagen Ethereum Meetup Jacob youtu.be/arecj2vyjlE\n"
        "Tackling Scalability Panel youtu.be/AH2g-KpPk7w\n\n"
        "uRaiden videos:\n"
        "uRaiden presentation Devcon3: youtu.be/yx0__aFvjzk?t=9m35s\n"
        "uRaiden Berlin Meetup drone demo: youtube.com/watch?v=E6CIgJPxgpQ\n"
        "ScalingNOW! Loredana talk: youtu.be/81gK-5qLFeg\n"
        "Feel free to PM me @RaidenCommunityInfoBot"
        ,disable_web_page_preview=1)



###### Error logging
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)




def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("events", events))
    dp.add_handler(CommandHandler("videos", videos))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
