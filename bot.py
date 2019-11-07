import telebot
import os
import sqlite3
import logging
from googletrans import Translator
import tempfile
import json

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


def db_query(sql, commit=False):
    conn = sqlite3.connect("data/word_base.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    if commit:
        conn.commit()
    conn.close()


def main():

    if not os.path.isdir("data"):
        os.mkdir("data")

    db_query("""CREATE TABLE IF NOT EXISTS words
                (user_id integer, word text, translation text)""")

    api_key = os.getenv("TELEGRAM_TOKEN", "")

    if not api_key:
        log.info("Please set env var TELEGRAM_TOKEN")
        exit(1)

    bot = telebot.TeleBot(api_key)

    @bot.message_handler(commands=['dict'])
    def print_dict(message):
        """
        Returns users dictionary
        if command /dict provided
        """
        conn = sqlite3.connect("data/word_base.db")
        cursor = conn.cursor()
        user_id = message.chat.id
        cursor.execute(f"select * from words where user_id = {user_id}")
        user_dict = cursor.fetchall()

        bot.send_message(message.chat.id, json.dumps(user_dict, indent=4))

        file, path = tempfile.mkstemp(suffix=".txt")
        with open(path, "w") as f:
            data = ""
            for line in user_dict:
                data = f"{data}\n{line[1]}:{line[2]}"
            f.write(data)
        with open(path, "r") as f:
            bot.send_document(message.chat.id, f, caption="dict.txt")

    @bot.message_handler()
    def add_word(message):
        """
        Add new word/phrase to dictionary
        with it's translation
        """
        new_word = message.text.capitalize()

        translator = Translator()
        translated_word = translator.translate(new_word, dest='ru').text.capitalize()
        bot.send_message(message.chat.id, f"Word {new_word!r} as {translated_word!r} added to dictionary. ")

        db_query(f"INSERT INTO words VALUES ({message.chat.id}, '{new_word}', '{translated_word}')", commit=True)

    bot.polling()


if __name__ == '__main__':
    main()
