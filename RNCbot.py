from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
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




def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)




def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("events", events))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
