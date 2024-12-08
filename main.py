from dotenv import load_dotenv
import os
import threading
import db
import telegram
import scraper

if __name__ == "__main__":
    load_dotenv()
    db.init_db()
    telegram.init_bot(os.getenv("TOKEN"))
    polling_thread = threading.Thread(target=telegram.start_polling)
    polling_thread.start()
    scraping_thread = threading.Thread(target=scraper.scrape)
    scraping_thread.start()
    print("Initialized")