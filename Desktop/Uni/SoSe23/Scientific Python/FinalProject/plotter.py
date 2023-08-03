import requests
from bs4 import BeautifulSoup
import os
from tqdm.notebook import tqdm
import pandas as pd
from loguru import logger
import time
import datetime
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

class DataFramePlotter:
    def __init__(self):

        # print('Launched Dataframe-Plotter')
        self.folder_name = "images/" + date.today().strftime("%Y/%m/%d") + '/'
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        


    def plot_amount_categories_MW(self, df) -> str:
        image_name = self.folder_name + 'amounts_category_MW.jpg'
        x = ['women', 'men']
        df = df[df['overview'] == 1]
        # print(len(df))

        count_m = df['gender'].value_counts().get('m')
        count_w = df['gender'].value_counts().get('w')
        y = [count_w, count_m]
        ax = sns.barplot(x=x, y=y, linewidth=0.5)

        current_date = datetime.datetime.now().date()
        ax.set_title(f'Amount of categories M vs W as of {current_date}', size=10)
        
        # set labels
        ax.set_xlabel('gender', size=12)
        ax.set_ylabel('nr categories', size=12)
        fig = ax.get_figure()
        fig.savefig(image_name)
        return image_name
        # plt.clf()

    def plot_amount_announces_per_category(self, df) -> str:
        image_name = self.folder_name + 'amounts_per_category.jpg'

        df = df[df['overview'] == 1]
        df = df[df['title'] != '']
        df = df[df['item_count'] != '']
        df['item_count'] = df['item_count'].astype(int)
        df_sorted = df.sort_values('item_count', ascending=False)
        df_sorted = df_sorted.head(50)
        fig, ax = plt.subplots(figsize=(40, 20))
        sns.barplot(data=df_sorted, x='title',y='item_count', ax=ax)

        current_date = datetime.datetime.now().date()
        ax.set_title(f'Amount of announces per category as of {current_date}', size=30)
        
        # set labels
        ax.set_xlabel('Category', size=20)
        ax.set_ylabel('amount announces', size=20)

        ax.set_xticklabels(ax.get_xticklabels(), size=18)
        ax.set_yticklabels(ax.get_yticklabels(), size=18)
        # ax.get_yaxis().get_major_formatter().set_scientific(False)
        # Define a function to format y axis values
        format_func = lambda x, _: '{:,.0f}'.format(x)
        ax.get_yaxis().set_major_formatter(FuncFormatter(format_func))
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        
        fig.savefig(image_name)
        return image_name


    def plot_average_price_per_category(self, df) -> str:

        image_name = self.folder_name + 'average_price_per_category.jpg'

        df = df[df['overview'] == 0].copy()

        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna(subset=['price'])
        df['price'] = df['price'].astype(np.float32)


        df['price'] = df['price'].astype(str)
        df['price'] = df['price'].str.replace('[^0-9.]', '', regex=True)
        df['price'] = df['price'].astype(float)
        df = df.groupby('cat_title')['price'].mean().reset_index()

        df['price'] = df['price'].astype(int)
        df_sorted = df.sort_values('price', ascending=False)
        df_sorted = df_sorted.head(50)

        fig, ax = plt.subplots(figsize=(40, 20))
        sns.barplot(data=df_sorted, x='cat_title',y='price', ax=ax)


 # format title with current date
        current_date = datetime.datetime.now().date()
        ax.set_title(f'Average Price Per Category as of {current_date}', size=30)
        
        # set labels
        ax.set_xlabel('Category', size=20)
        ax.set_ylabel('Average Price', size=20)

        ax.set_xticklabels(ax.get_xticklabels(), size=18)
        ax.set_yticklabels(ax.get_yticklabels(), size=18)
        # ax.get_yaxis().get_major_formatter().set_scientific(False)
        format_func = lambda x, _: '{:,.0f}'.format(x)
        ax.get_yaxis().set_major_formatter(FuncFormatter(format_func))
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        fig.savefig(image_name)
        return image_name


    def plot_announces_per_user(self, df) -> str:

        image_name = self.folder_name + 'announces_per_user_top200.jpg'

        df = df[df['overview'] == 0].copy()
        df = df['login'].value_counts().sort_values(ascending=False)

        logger.debug(df.head())
        # Split data into three groups
        first_200 = df[:50].reset_index()
        # logger.debug(first_200.head())
        # next_200 = df[200:400].reset_index()
        # rest = df[400:].reset_index()
        # print(first_200)
        # df_sorted = df_sorted.head(50)
        # Plot the first 200
        fig, ax = plt.subplots(figsize=(40,20))
        sns.barplot(data=first_200, x='login', y='count')


        current_date = datetime.datetime.now().date()
        ax.set_title(f'Announces per user as of {current_date}', size=30)
        
        # set labels
        ax.set_xlabel('Category', size=20)
        ax.set_ylabel('Average Price', size=20)

        ax.set_xticklabels(ax.get_xticklabels(), size=18)
   
        ax.set_yticklabels(ax.get_yticklabels(), size=18)
        # ax.get_yaxis().get_major_formatter().set_scientific(False)
        format_func = lambda x, _: '{:,.0f}'.format(x)
        ax.get_yaxis().set_major_formatter(FuncFormatter(format_func))
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        fig.savefig(image_name)
        return image_name

