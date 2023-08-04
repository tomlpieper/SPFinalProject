import os
from telebot import types
import telebot
import requests
import pandas as pd
from loguru import logger
from datetime import date


class TelegramBotAPI():
    """
    Class to handle operations of a Telegram Bot for data analysis of vinted.de.

    Attributes
    ----------
    bot : telebot
        Instance of telebot class
    db_connector : Object
        Our class instance to handle database related operations
    scraper : Object
        class instance to handle data scraping from website
    plotter : Object
        class instance to handle data plotting operations
    df : pandas.DataFrame
        DataFrame to store scraped data


    Note: 
        All instances of the here given classes are defined in main.py
    """

    def __init__(self, token, db_connector, scraper, plotter):
        """ 
        Constructor for the TelegramBotAPI class

        Parameters:
        ----------
        token (str): token for telegram bot
        db_connector (obj): instance of database connector
        scraper (obj): instance of web scraper
        plotter (obj): instance of plot generator
        """
        self.bot = telebot.TeleBot(token)
        self.db_connector = db_connector
        self.scraper = scraper
        self.plotter = plotter
        self.bot.message_handler(commands=['start', 'init'])(self.init_analysis)
        self.df = None  # Initial DataFrame set to None

    def init_analysis(self,message):
        """
        Method to initialize analysis by asking the user to choose between today's analysis and a different date.

        Parameters:
        ----------
        message (obj): message from the user
        """
        # Reset DataFrame to None at the start of a new analysis
        self.df = None

        keys = ['Yes', 'No I want another date.']
        self.bot.reply_to(message, "Welcome to the analysis of vinted.de.")
        # Create a response keyboard
        keyboard = types.ReplyKeyboardMarkup(row_width=3)
        buttons = [types.KeyboardButton(key) for key in keys]
        keyboard.add(*buttons)
        self.bot.send_message(message.chat.id, "Would you like todays analysis?", reply_markup=keyboard)
        # Register the next step handler
        self.bot.register_next_step_handler(message,self.binary_handler)

    def binary_handler(self, message):
        """
        Handler for the binary response of the user (Yes or No). This will decide the next course of action.

        Parameters:
        ----------
        message (obj): message from the user
        """
        if message.text == 'Yes':
            # Handle 'Yes' response, i.e., user wants today's analysis
            data = self.db_connector.retrieve_data(date.today())
            if not data.empty: # if data for today is available
                self.df = data
                self.ask_for_analysis_type(message)
            else: # if no data for today, ask if user wants to scrape data
                self.ask_for_scraping(message)
        elif message.text == 'No I want another date.':
            # Handle 'No' response, i.e., user wants analysis of some other date
            self.ask_for_date(message)

    def ask_for_scraping(self, message):
        """
        Method to ask the user if they want to scrape data for today

        Parameters:
        ----------
        message (obj): message from the user
        """

        # the keyboard modifications is supposed to simplify the users interaction with the bot and is directly shown in Telegram
        keys = ['Yes', 'No']
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        buttons = [types.KeyboardButton(key) for key in keys]
        keyboard.add(*buttons)
        self.bot.send_message(message.chat.id, "No data available for today. Would you like to scrape data now?", reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.scraping_handler)

    def scraping_handler(self, message):
        """
        Handler to decide the next course of action based on user's response to data scraping

        Parameters:
        ----------
        message (obj): message from the user
        """
        if message.text == 'Yes':
            # If user wants to scrape data, do it and then ask for type of analysis
            self.bot.send_message(message.chat.id, "Scraping data from vinted.de... this could take a couple of hours. I will notify you when the data is available.")
            data = self.scraper.scrape(scheduled=False)
            if not data.empty: # Data found after scraping
                self.df = data
                self.ask_for_analysis_type(message)
            else:
                # If there's still no data after scraping, inform the user and ask for another date or command
                self.bot.send_message(message.chat.id, "No data could be scraped. Please choose another date or command.")
        else:
            # If user doesn't want to scrape data, ask for another date
            self.ask_for_date(message)

    def ask_for_date(self, message):
        """
        Method to ask the user for a date input

        Parameters:
        ----------
        message (obj): message from the user
        """
        markup = types.ReplyKeyboardRemove(selective=False)
        sent_msg = self.bot.send_message(message.chat.id, "Please enter the date in the format DD/MM/YYYY.", reply_markup=markup)
        self.bot.register_next_step_handler(sent_msg, self.date_handler)

    def date_handler(self, message):
        """
        Handler to process the date input by the user and decide the next course of action

        Parameters:
        ----------
        message (obj): message from the user
        """
        date_input = message.text
        data = self.db_connector.retrieve_data(date_input)
        if not data.empty: # Data found for the specified date
            self.df = data
            self.ask_for_analysis_type(message)
        else:
            # If no data for the specified date, inform the user and ask for another command
            self.bot.send_message(message.chat.id, "No data available for the specified date. Please choose another date or command.")
            self.bot.register_next_step_handler(message, self.init_analysis) 

    def ask_for_analysis_type(self, message):
        """
        Method to ask the user for the type of analysis they want

        Parameters:
        ----------
        message (obj): message from the user
        """
        analysis_types = ['Full analysis', 'amount of categories men vs women', 'amount anounces per category', 'average price per category', 'announces per user']
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        buttons = [types.KeyboardButton(analysis_type) for analysis_type in analysis_types]
        keyboard.add(*buttons)
        sent_msg = self.bot.send_message(message.chat.id, "Your Data is ready for analysis! Please select the type of analysis.", reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_msg, self.analysis_type_handler)

    def analysis_type_handler(self, message):
        """
        Handler to process the type of analysis selected by the user and provide the respective analysis

        Parameters:
        ----------
        message (obj): message from the user
        """
        analysis_type = message.text
        # Multiple if-else statements to handle different types of analyses, Full Analysis just returns all combined
        # Each analysis type will generate a different plot

        if analysis_type == 'Full analysis':
            # generate the plot based on the selected type
            path_1= self.plotter.plot_amount_categories_MW(self.df)  # assume this method returns the path to the plot image
            photo_1 = open(path_1, 'rb')
            self.bot.send_photo(message.chat.id, photo_1)

            path_2= self.plotter.plot_amount_announces_per_category(self.df)  # assume this method returns the path to the plot image
            photo_2 = open(path_2, 'rb')
            self.bot.send_photo(message.chat.id, photo_2)

            path_3= self.plotter.plot_average_price_per_category(self.df)  # assume this method returns the path to the plot image
            photo_3 = open(path_3, 'rb')
            self.bot.send_photo(message.chat.id, photo_3)

            path_4= self.plotter.plot_announces_per_user(self.df)  # assume this method returns the path to the plot image
            photo_4 = open(path_4, 'rb')
            self.bot.send_photo(message.chat.id, photo_4)

        elif analysis_type == 'amount of categories men vs women':
            path= self.plotter.plot_amount_categories_MW(self.df)  # assume this method returns the path to the plot image
            photo = open(path, 'rb')
            self.bot.send_photo(message.chat.id, photo)

        elif analysis_type == 'amount anounces per category':
            path= self.plotter.plot_amount_announces_per_category(self.df)  # assume this method returns the path to the plot image
            photo = open(path, 'rb')
            self.bot.send_photo(message.chat.id, photo)
        
        elif analysis_type == 'average price per category': 
            path= self.plotter.plot_average_price_per_category(self.df)  # assume this method returns the path to the plot image
            photo = open(path, 'rb')
            self.bot.send_photo(message.chat.id, photo)
        
        elif analysis_type == 'announces per user': 
            path= self.plotter.plot_announces_per_user(self.df)  # assume this method returns the path to the plot image
            photo = open(path, 'rb')
            self.bot.send_photo(message.chat.id, photo)

        self.bot.register_next_step_handler(message, self.init_analysis)




    def launch(self):
        # Launch the bot with internal function infinity polling, that constantly listens to user messages
        self.bot.infinity_polling()
