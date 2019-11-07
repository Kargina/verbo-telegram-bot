import telebot
# from telebot import types
import os
import sqlite3
import logging
from googletrans import Translator

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


def main():
    if not os.path.isdir("data"):
        os.mkdir("data")
    conn = sqlite3.connect("data/word_base.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS words
                             (user_id integer, word text, translation text)
                          """)
    conn.close()

    api_key = os.getenv("TELEGRAM_TOKEN", "")
    if not api_key:
        log.info("Please set env var TELEGRAM_TOKEN")
        exit(1)

    bot = telebot.TeleBot(api_key)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """Test function"""
        bot.send_message(message.chat.id, "Hi! How are you doing?")

    @bot.message_handler(commands=['dict'])
    def print_dict(message):
        """Returns users dictionary
           if command /dict provided"""
        conn = sqlite3.connect("data/word_base.db")
        cursor = conn.cursor()
        user_id = message.chat.id
        cursor.execute(f"select * from words where user_id = {user_id}")
        user_dict = cursor.fetchall()
        for line in user_dict:
            bot.send_message(message.chat.id, line[1] + " - " + line[2])
        conn.close()

    @bot.message_handler()
    def add_word(message):
        """Add new word/phrase to dictionary
           with it's translation"""
        new_word = message.text.capitalize()

        conn = sqlite3.connect("data/word_base.db")
        cursor = conn.cursor()

        translator = Translator()
        translated_word = translator.translate(new_word, dest='ru').text.capitalize()

        bot.send_message(message.chat.id, f"Adding word '{new_word}' as '{translated_word}' to dictionary. ")

        cursor.execute(f"INSERT INTO words VALUES ({message.chat.id}, '{new_word}', '{translated_word}')")
        conn.commit()
        conn.close()

    bot.polling()


if __name__ == '__main__':
    main()
