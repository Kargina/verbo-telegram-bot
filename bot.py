import telebot
import os
import sqlite3
import logging
from db import DB
from googletrans import Translator

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def main():

    # db = DB("jhjhj.hhjh")

    api_key = os.getenv("TELEGRAM_TOKEN", "")

    if not api_key:
        log.info("Please set env var TELEGRAM_TOKEN")
        exec(1)

    bot = telebot.TeleBot(api_key)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "Howdy, how are you doing?")

    @bot.message_handler(commands=['dict'])
    def print_dict(message):
        conn = sqlite3.connect("data/word_base.db")
        cursor = conn.cursor()
        user_id = message.chat.id
        cursor.execute(f"select * from words where user_id = {user_id}")
        user_dict = cursor.fetchall()
        for line in user_dict:
            bot.send_message(message.chat.id, line[1] + " - " + line[2])

    @bot.message_handler()
    def add_word(message):
        new_word = message.text.capitalize()

        conn = sqlite3.connect("data/word_base.db")
        cursor = conn.cursor()

        translator = Translator()
        translated_word = translator.translate(new_word, dest='ru').text.capitalize()

        bot.send_message(message.chat.id, f"Adding word '{new_word}' as '{translated_word}' to dictionary. ")

        cursor.execute(f"INSERT INTO words VALUES ({message.chat.id}, '{new_word}', '{translated_word}')")
        conn.commit()

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