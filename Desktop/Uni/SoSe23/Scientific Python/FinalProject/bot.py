import os

from telebot import types
import telebot
import requests




class TelegramBotAPI():

    def __init__(self, token, db_connector, scraper, plotter):
        self.bot = telebot.TeleBot(token)
        self.db_connector = db_connector
        self.scraper = scraper
        self.plotter = plotter
        self.bot.message_handler(commands=['start', 'hello'])(self.send_welcome)
        self.bot.message_handler(commands=['horoscope'])(self.sign_handler)

    

    # @bot.message_handler(commands=['start', 'hello'])
    def send_welcome(self,message):
        bot.reply_to(message, "Howdy, how are you doing?")

    # @bot.message_handler(commands=['horoscope'])
    def sign_handler(self,message):
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        keyboard = types.ReplyKeyboardMarkup(row_width=3)  # create keyboard, set row_width to your liking
        buttons = [types.KeyboardButton(sign) for sign in signs]  # create a button for each sign
        keyboard.add(*buttons)  # add all buttons to the keyboard
        self.bot.send_message(message.chat.id, "What's your zodiac sign?", reply_markup=keyboard)
        self.bot.register_next_step_handler(message, self.day_handler)


    def day_handler(self, message):
        sign = message.text
        days = ["TODAY", "TOMORROW", "YESTERDAY"]
        keyboard = types.ReplyKeyboardMarkup(row_width=1)  # create keyboard, set row_width to your liking
        buttons = [types.KeyboardButton(day) for day in days]  # create a button for each day
        keyboard.add(*buttons)  # add all buttons to the keyboard
        sent_msg = self.bot.send_message(message.chat.id, "What day do you want to know?", reply_markup=keyboard)
        self.bot.register_next_step_handler(sent_msg, self.fetch_horoscope, sign.capitalize())



    def fetch_horoscope(self,message, sign):
        day = message.text
        horoscope = self.get_daily_horoscope(sign, day)
        data = horoscope["data"]
        horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}\\n*Day:* {data["date"]}'
        self.bot.send_message(message.chat.id, "Here's your horoscope!")
        markup = types.ReplyKeyboardRemove(selective=False)
        self.bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown", reply_markup=markup)



    def get_daily_horoscope(self, sign: str, day: str) -> dict:
        """Get daily horoscope for a zodiac sign.
        Keyword arguments:
        sign:str - Zodiac sign
        day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
        Return:dict - JSON data
        """
        url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
        params = {"sign": sign, "day": day}
        response = requests.get(url, params)

        return response.json()

    def launch(self):
        self.bot.infinity_polling()
