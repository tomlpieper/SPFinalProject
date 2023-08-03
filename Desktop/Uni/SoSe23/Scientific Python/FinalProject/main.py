from pymongo import MongoClient
from plotter import DataFramePlotter
from bot import TelegramBotAPI
from db_connector import DB_Connector
from scraper import Scraper
from loguru import logger
import os
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz

# def function_to_schedule():
#     # your function here
    

def start_scheduler(scraper):
    scheduler = BackgroundScheduler()

    # Timezone definition
    tz = pytz.timezone('Europe/Berlin') # e.g. 'America/New_York'

    # Calculate next 6 AM in your timezone
    next_6_am = datetime.now(tz).replace(hour=6, minute=0, second=0, microsecond=0)
    if next_6_am < datetime.now(tz):
        next_6_am += timedelta(days=1)

    # Schedule job
    scheduler.add_job(scraper.scrape, 'interval', days=1, start_date=str(next_6_am), kwargs={'scheduled': True})

    # Start the scheduler
    scheduler.start()










if __name__ == "__main__":


    # Run and Init all of them

    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    hostname = os.environ['MONGO_HOSTNAME']

    db_connector = DB_Connector(username=username, password=password, hostname=hostname)
    logger.debug('DB Connector Initialized')

    scraper = Scraper(db_connector=db_connector)
    logger.debug('Scraper Initialized')

    start_scheduler(scraper=scraper)
    logger.debug('Schedule for scraping Initialized')

    # # Here we need to scrape before plotting
    plotter = DataFramePlotter()

    bot = TelegramBotAPI(token='6621867212:AAEK9MPsdcH7iYw0guYYtHZJ1cdo_EcJBk8',db_connector=db_connector,scraper=scraper, plotter=plotter)
    logger.debug('Bot Initialized')
    t = threading.Thread(target=bot.launch)
    t.start()
    # bot.launch()
    logger.debug('Bot Launched')


