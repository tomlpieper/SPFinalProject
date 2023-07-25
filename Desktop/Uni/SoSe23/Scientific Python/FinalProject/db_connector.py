
import os
import time
from datetime import date
from pymongo import MongoClient
import pandas as pd



class DB_Connector():

    def __init__(self, username, password, hostname):

        self.username = username
        self.password = password
        self.hostname = hostname

        self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.hostname}:27017/')
        # Use a database named "mydatabase"
        self.db = self.client["mydatabase"]
        
        # Use a collection (similar to a table in SQL) named "customers"
        self.collection = self.db["customers"]

        print('Connected to Database',flush=True)



    def test_save_and_retrieve_data(self):
        # Create a connection
        # Define some data to save
        customer_data = {"name": "John", "address": "Highway 37"}
        
        # Save the data
        collection.insert_one(customer_data)
        
        # Retrieve the data
        result = collection.find_one({"name": "John"})
        
        # Check that the data is as expected
        # print(assert result["name"] == "John")
        assert result["name"] == "John"
        print(result)
        assert result["address"] == "Highway 37"

    def save_data(self, dataframe):

        
        data_dict = dataframe.to_dict("records")
        today = date.today()
        timestamp = today.strftime("%d/%m/%Y")
        for data in data_dict:
            data['timestamp'] = timestamp

        validation_doc = self.collection.find_one({'timestamp': timestamp})
        if not validation_doc:
            self.collection.insert_many(data_dict)
            print('Successfully saved documents to database.')
        else: 
            print('Already saved Data today, nothing is saved')



    def retrieve_data(self,date):
        # today = date.today()
        timestamp = date.strftime("%d/%m/%Y")
        r = self.collection.find({'timestamp': timestamp})
        docs = [doc for doc in r]
        return docs


# # Insert the data into the collection
# # collection.insert_many(data_dict)