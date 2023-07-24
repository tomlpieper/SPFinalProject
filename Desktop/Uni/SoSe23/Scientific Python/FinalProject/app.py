import os
import time
from pymongo import MongoClient
from db_connector import DB_Connector

# print('Hello World',flush=True)

# Get MongoDB username, password, and hostname from environment variables
username = os.environ['MONGO_USERNAME']
password = os.environ['MONGO_PASSWORD']
hostname = os.environ['MONGO_HOSTNAME']

# # Connect to MongoDB
# # client = MongoClient(f'mongodb://{username}:{password}@{hostname}:27017/')
# # db = client['test-database']
# # collection = db['test-collection']

# def test_save_and_retrieve_data():
#     # Create a connection
#     client = MongoClient(f'mongodb://{username}:{password}@{hostname}:27017/')
    
#     # Use a database named "mydatabase"
#     db = client["mydatabase"]
    
#     # Use a collection (similar to a table in SQL) named "customers"
#     collection = db["customers"]
    
#     # Define some data to save
#     customer_data = {"name": "John", "address": "Highway 37"}
    
#     # Save the data
#     collection.insert_one(customer_data)
    
#     # Retrieve the data
#     result = collection.find_one({"name": "John"})
    
#     # Check that the data is as expected
#     # print(assert result["name"] == "John")
#     assert result["name"] == "John"
#     print(result)
#     assert result["address"] == "Highway 37"


    
#     # Close the connection
#     client.close()

# test_save_and_retrieve_data()

c = DB_Connector(username, password, hostname)
c.test_save_and_retrieve_data()

while True:
    print('Hello world',flush=True)
    time.sleep(5)