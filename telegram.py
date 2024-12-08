import telebot
import asyncio
import sqlite3

bot = None

def init_bot(token):
    global bot
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        with sqlite3.connect('sqlite3.db') as db_con:
            db_con.execute(f"INSERT INTO subscriptions VALUES ({message.chat.id})")
            print(f"Inserted {message.chat.id} into DB")
        bot.reply_to(message, "Subscribed to notifications")


    @bot.message_handler(commands=["stop"])
    def send_welcome(message):
        with sqlite3.connect('sqlite3.db') as db_con:
            db_con.execute(f"DELETE FROM subscriptions WHERE chatid={message.chat.id}")
            print(f"Removed {message.chat.id} from DB")
        bot.reply_to(message, "Removed from notifications")


def start_polling():
    bot.infinity_polling()


def notify_all():
    print("Notifying all...")
    with sqlite3.connect('sqlite3.db') as db_con:
        cur = db_con.execute("SELECT chatid FROM subscriptions")
        rows = cur.fetchall()
    chat_ids = list(map(lambda x: x[0], rows))
    for chat_id in chat_ids:
        print(f"Notifying {chat_id}")
        bot.send_message(chat_id, "stock available")
