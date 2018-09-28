import telebot


bot = telebot.TeleBot("")


ADMINS                      = ['']

############  Bot error handler
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


############  Restrict bot functions to admins
def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped




############  Resolve message data to a readable name 	 		
def get_name(user):
        try:
            name = user.first_name
        except (NameError, AttributeError):
            try:
                name = user.username
            except (NameError, AttributeError):
                logger.info("No username or first name.. wtf")
                return	""
        return name


########### COMMANDS


########### replies

@bot.message_handler(commands=['start', 'help', 'heybot'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")





########### Invalid

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, "Invalid command")




############ Restricted






bot.polling()
