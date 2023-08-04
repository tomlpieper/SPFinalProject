import os
import time
from datetime import date
from pymongo import MongoClient
import pandas as pd
from loguru import logger


class DB_Connector():
    """
    Database connector class which connects to MongoDB and provides methods to save and retrieve data.
    """

    def __init__(self, username, password, hostname):
        """
        Initialize the database connector with MongoDB connection details.

        Parameters:
        ----------
        username (str): username of the db
        hostanem (str): password of the db
        password (str): hostname of the db
        """

        self.username = username
        self.password = password
        self.hostname = hostname

        # Establish a connection with MongoDB
        self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.hostname}:27017/')
        
        # Use a database named "mydatabase"
        self.db = self.client["mydatabase"]
        
        # Use a collection (similar to a table in SQL) named "customers"
        self.collection = self.db["scrapes"]

        print('Connected to Database', flush=True)

    def save_data(self, dataframe):
        """
        Save the data in the provided dataframe to MongoDB.

        Parameters:
        ----------
        dataframe (pandas.df): dataframe with data to save
        """

        # Convert dataframe to a list of dictionaries
        data_dict = dataframe.to_dict("records")
        
        # Get today's date and format it as DD/MM/YYYY
        today = date.today()
        timestamp = today.strftime("%d/%m/%Y")
        
        # Add a timestamp to each dictionary
        for data in data_dict:
            data['timestamp'] = timestamp

        # Check if data for today has already been saved
        validation_doc = self.collection.find_one({'timestamp': timestamp})
        
        # If not, insert the data into the database
        if not validation_doc:
            self.collection.insert_many(data_dict)
            logger.success('Successfully saved documents to database.')
        else: 
            # If data for today has already been saved, log a warning
            logger.warning('Already saved Data today, nothing is saved')

    def retrieve_data(self, date):
        """
        Retrieve data for the specified date from MongoDB. Returns pandas.df

        Parameters:
        ----------
        date (date/str): date to retrieve data from
        """

        # Format the date as DD/MM/YYYY
        if not isinstance(date, str):
            timestamp = date.strftime("%d/%m/%Y")
        else: 
            timestamp = date
        
        # Retrieve documents from the collection where timestamp matches the specified date
        r = self.collection.find({'timestamp': timestamp})
        
        # Create a list of all retrieved documents
        docs = [doc for doc in r]

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(docs)

        return df
