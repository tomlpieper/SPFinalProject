import os
from telebot import types
import telebot
import requests
import pandas as pd
from loguru import logger
from datetime import date




class TelegramBotAPI():

    def __init__(self, token, db_connector, scraper, plotter):
        self.bot = telebot.TeleBot(token)
        self.db_connector = db_connector
        self.scraper = scraper
        self.plotter = plotter
        self.bot.message_handler(commands=['start', 'init'])(self.init_analysis)
        self.df = None
        # self.bot.message_handler(commands=['horoscope'])(self.sign_handler)

    

    def init_analysis(self,message):
        self.df = None
        keys = ['Yes', 'No I want another date.']
        self.bot.reply_to(message, "Welcome to the analysis of vinted.de.")
        keyboard = types.ReplyKeyboardMarkup(row_width=3)  # create keyboard, set row_width to your liking
        buttons = [types.KeyboardButton(key) for key in keys]  # create a button for each sign
        keyboard.add(*buttons)  # add all buttons to the keyboard
        self.bot.send_message(message.chat.id, "Would you like todays analysis?", reply_markup=keyboard)
        self.bot.register_next_step_handler(message,self.binary_handler)

    def binary_handler(self, message):
        if message.text == 'Yes':
            # if user chooses today's analysis, you could check the database and continue accordingly
            data = self.db_connector.retrieve_data(date.today()) # check data for today's date
            if not data.empty: # data found for today
                # ask for type of analysis
                self.df = data
                self.ask_for_analysis_type(message)
            else:
                # if there's no data for today, ask user if they want to scrape data
                self.ask_for_scraping(message)
        elif message.text == 'No I want another date.':
            # if user wants another date's analysis, call a method to handle date input
            self.ask_for_date(message)

    def ask_for_scraping(self, message):
        # ask the user if they want to scrape data for today
        keys = ['Yes', 'No']
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        buttons = [types.KeyboardButton(key) for key in keys]
        keyboard.add(*buttons)
        self.bot.send_message(message.chat.id, "No data available for today. Would you like to scrape data now?", reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.scraping_handler)

    def scraping_handler(self, message):
        if message.text == 'Yes':
            # if user wants to scrape data, do it and then ask for type of analysis
            self.bot.send_message(message.chat.id, "Scraping data from vinted.de... this could take a couple of hours. I will notify you when the data is available.")
            data = self.scraper.scrape(scheduled=False) # you need to implement this method
            if not data.empty: # data found after scraping
                # ask for type of analysis
                self.df = data
                self.ask_for_analysis_type(message)
            else:
                # if there's still no data after scraping, you might want to inform the user and ask for another command
                self.bot.send_message(message.chat.id, "No data could be scraped. Please choose another date or command.")
        else:
            # if user doesn't want to scrape data, ask for another date
            self.ask_for_date(message)


    def ask_for_date(self, message):
        # you might want to call a date picker keyboard or just simply ask the user to input the date in a specific format
        # here is a simple way of asking the user to input the date
        markup = types.ReplyKeyboardRemove(selective=False)
        sent_msg = self.bot.send_message(message.chat.id, "Please enter the date in the format DD/MM/YYYY.", reply_markup=markup)
        self.bot.register_next_step_handler(sent_msg, self.date_handler)

    def date_handler(self, message):
        date = message.text
        # check the database for this date
        data = self.db_connector.retrieve_data(date)
        if not data.empty: # data found for specified date
            # ask for type of analysis
            self.df = data
            self.ask_for_analysis_type(message)
        else:
            # if there's no data for the specified date, you might want to inform the user and ask for another command
            self.bot.send_message(message.chat.id, "No data available for the specified date. Please choose another date or command.")
            self.bot.register_next_step_handler(message, self.init_analysis) 

    def ask_for_analysis_type(self, message):
        # ask the user to select the type of analysis they want
        analysis_types = ['Full analysis', 'amount of categories men vs women', 'amount anounces per category', 'average price per category', 'announces per user']
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        buttons = [types.KeyboardButton(analysis_type) for analysis_type in analysis_types]
        keyboard.add(*buttons)
        sent_msg = self.bot.send_message(message.chat.id, "Your Data is ready for analysis! Please select the type of analysis.", reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_msg, self.analysis_type_handler)

    def analysis_type_handler(self, message):
        analysis_type = message.text


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
        # logger.debug('Launched Bot')
        self.bot.infinity_polling()
