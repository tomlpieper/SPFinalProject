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

class DataFramePlotter:
    def __init__(self, df):
        self.df = df
        # print('Launched Dataframe-Plotter')
        self.folder_name = "images/" + date.today().strftime("%Y/%m/%d") + '/'
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        


    def plot_amount_categories_MW(self):
        image_name = self.folder_name + 'amounts_category_MW.jpg'
        x = ['women', 'men']
        df = self.df[self.df['overview'] == 1]
        print(len(df))

        count_m = df['gender'].value_counts().get('m')
        count_w = df['gender'].value_counts().get('w')
        y = [count_w, count_m]
        ax = sns.barplot(x=x, y=y, linewidth=0.5)
        fig = ax.get_figure()
        fig.savefig(image_name)
        # plt.clf()

    def plot_amount_announces_per_category(self):
        image_name = self.folder_name + 'amounts_per_category.jpg'

        df = self.df[self.df['overview'] == 1]
        df = df[df['title'] != '']
        df = df[df['item_count'] != '']
        df['item_count'] = df['item_count'].astype(int)
        df_sorted = df.sort_values('item_count', ascending=False)
        fig, ax = plt.subplots(figsize=(40, 20))
        sns.barplot(data=df_sorted, x='title',y='item_count', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), size=8)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        
        fig.savefig(image_name)


    def plot_average_price_per_category(self):

        image_name = self.folder_name + 'average_price_per_category.jpg'

        df = self.df[self.df['overview'] == 0].copy()

        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df.dropna(subset=['price'])
        df['price'] = df['price'].astype(np.float32)


        df['price'] = df['price'].astype(str)
        df['price'] = df['price'].str.replace('[^0-9.]', '', regex=True)
        df['price'] = df['price'].astype(float)
        df = df.groupby('cat_title')['price'].mean().reset_index()

        df['price'] = df['price'].astype(int)
        df_sorted = df.sort_values('price', ascending=False)

        fig, ax = plt.subplots(figsize=(40, 20))
        sns.barplot(data=df_sorted, x='cat_title',y='price', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), size=8)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        for item in ax.get_xticklabels():
            item.set_rotation(90)
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        fig.savefig(image_name)


    def plot_announces_per_user(self):

        image_name = self.folder_name + 'announces_per_user_top200.jpg'

        df = self.df[self.df['overview'] == 0].copy()
        df = df['login'].value_counts().sort_values(ascending=False)

        logger.debug(df.shape[0])
        # Split data into three groups
        first_200 = df[:200].reset_index()
        # next_200 = df[200:400].reset_index()
        # rest = df[400:].reset_index()
        # print(first_200)

        # Plot the first 200
        fig, ax = plt.subplots(figsize=(40,20))
        sns.barplot(data=first_200, x='index', y='login')
        plt.title('Top 200 Users')
        plt.xlabel('Users')
        plt.ylabel('Counts')
        plt.xticks(rotation=90)
        plt.show()
        plt.subplots_adjust(bottom=0.3)
        fig = ax.get_figure()
        fig.savefig(image_name)
