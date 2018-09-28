from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

###### Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



def start(bot, update):

    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)

def resources(bot, update):
    update.message.reply_text('Raiden Network resources:\n\n'

        'Website raiden.network/\n'
        'FAQ raiden.network/faq.html\n'
        'Github github.com/raiden-network/raiden\n'
        'Documentation readthedocs.org/projects/raiden-network/\n'
        'Specification PDF media.readthedocs.org/pdf/raiden-network-specification/latest/raiden-network-specification.pdf\n'
        'Medium Publications medium.com/@raiden_network\n'
        'Weekly Github Update reddit.com/user/bor4/posts/\n\n'

        'Feel free to PM me @RaidenCommunityInfoBot',disable_web_page_preview=1)

###### Log Errors caused by Updates.
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)



###### Run the bot
def main():
    updater = Updater("TOKEN")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
