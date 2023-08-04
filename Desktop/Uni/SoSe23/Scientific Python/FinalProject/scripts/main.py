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


def start_scheduler(scraper):
    """
    Function to start the scheduler to periodically run a web scraper
    """

    # Create an instance of the BackgroundScheduler
    scheduler = BackgroundScheduler()

    # Define the timezone
    tz = pytz.timezone('Europe/Berlin')

    # Calculate the next instance of 6AM in the given timezone
    next_6_am = datetime.now(tz).replace(hour=6, minute=0, second=0, microsecond=0)
    if next_6_am < datetime.now(tz):
        next_6_am += timedelta(days=1)

    # Add a job to the scheduler to run the web scraper at the calculated time
    scheduler.add_job(scraper.scrape, 'interval', days=1, start_date=str(next_6_am), kwargs={'scheduled': True})

    # Start the scheduler
    scheduler.start()


if __name__ == "__main__":
    """
    Main function where all components are initialized and run
    """

    # Retrieve MongoDB credentials from environment variables given in the docker-compose.yml
    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    hostname = os.environ['MONGO_HOSTNAME']

    # Initialize the DB connector
    db_connector = DB_Connector(username=username, password=password, hostname=hostname)
    logger.debug('DB Connector Initialized')

    # Initialize the web scraper with the DB connector
    scraper = Scraper(db_connector=db_connector)
    logger.debug('Scraper Initialized')

    # Start the scheduler with the web scraper
    start_scheduler(scraper=scraper)
    logger.debug('Schedule for scraping Initialized')

    # Initialize the data plotter
    plotter = DataFramePlotter()

    # Initialize the Telegram bot with the DB connector, scraper, and plotter
    bot = TelegramBotAPI(token='6621867212:AAEK9MPsdcH7iYw0guYYtHZJ1cdo_EcJBk8',db_connector=db_connector,scraper=scraper, plotter=plotter)
    logger.debug('Bot Initialized')
    
    # Launch the bot in a separate thread to be able to run different stuff after that 
    t = threading.Thread(target=bot.launch)
    t.start()
    
    logger.debug('Bot Launched')
