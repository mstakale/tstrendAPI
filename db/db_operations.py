import os
import sys
import pandas as pd
from pymongo import MongoClient

def create_database(database_name):
    # Set up MongoDB connection
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection URI
    db = client[database_name]  # Use the provided database name

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python main.py <database_name>")
    sys.exit(1)

# Get the database name from the command-line argument
db_name = sys.argv[1]

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection URI
db = client[db_name]  # Use the user-provided database name

# Directory containing CSV files (up one level to the "data" folder)
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Function to insert data into MongoDB
def insert_data(file_path, collection_name):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d') + pd.to_timedelta('00:00:00')
    collection = db[collection_name]
    collection.insert_many(data.to_dict("records"))

# Iterate through CSV files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        collection_name = os.path.splitext(filename)[0]  # Use the filename as the collection name
        insert_data(file_path, collection_name)

# Close MongoDB connection
client.close()

# Call the function to create the database
create_database(db_name)