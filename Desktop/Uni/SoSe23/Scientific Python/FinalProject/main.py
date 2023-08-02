from pymongo import MongoClient
from plotter import DataFramePlotter
from bot import TelegramBotAPI
from db_connector import DB_Connector
from scraper import Scraper
from loguru import logger
import os










if __name__ == "__main__":


    # Run and Init all of them

    username = os.environ['MONGO_USERNAME']
    password = os.environ['MONGO_PASSWORD']
    hostname = os.environ['MONGO_HOSTNAME']

    db_connector = DB_Connector(username=username, password=password, hostname=hostname)
    logger.debug('DB Connector Initialized')

    scraper = Scraper(db_connector=db_connector)
    logger.debug('Scraper Initialized')

    # dataframe = scraper.scrape()
    # # Here we need to scrape before plotting
    dataframe = None
    plotter = DataFramePlotter(df=dataframe)

    bot = TelegramBotAPI(token='6621867212:AAEK9MPsdcH7iYw0guYYtHZJ1cdo_EcJBk8',db_connector=db_connector,scraper=scraper, plotter=plotter)
    logger.debug('Bot Initialized')
    bot.launch()
    logger.debug('Bot Launched')