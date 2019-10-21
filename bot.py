import telebot
import os

api_key = "token"


def main():
    bot = telebot.TeleBot(api_key)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(commands=['dict'])
    def print_dict(message):
        path_to_file = "data/" + str(message.chat.id)
        dict_words = open(path_to_file)
        # bot.reply_to(message, dict_words)
        for line in dict_words:
            bot.reply_to(message, line)

    @bot.message_handler()
    def add_word(message):
        bot.reply_to(message, "Adding word to dictionary. " + "\n" +
                     "message.text: " + message.text + "\n"
                     "message.id: " + str(message.message_id) + "\n"
                     "message.chat.id: " + str(message.chat.id) + "\n")
                     # "message.length: " + str(message.length) + "\n")
        path_to_file = "data/" + str(message.chat.id)
        if os.path.exists(path_to_file):
            bot.reply_to(message, "User Exists!")
            with open(path_to_file, 'a') as f:
                print(message.text, file=f)

        else:
            bot.reply_to(message, "User NOT Exists!")
            with open(path_to_file, 'w') as f:
                print(message.text, file=f)

    bot.polling()


def test():
    dict_words = open("dict")
    # print(type(dict_words))
    # dict_words.read()
    for line in dict_words:
        print(line)


if __name__ == '__main__':
    main()
    # test()