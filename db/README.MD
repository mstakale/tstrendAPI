# CSV to MongoDB Timeseries Collection Import

This Python script allows you to easily import CSV files located in the "data" directory into a MongoDB database as timeseries collections. 

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (3.x recommended)
- pandas library (`pip install pandas`)
- pymongo library (`pip install pymongo`)
- MongoDB installed and running (`mongod`)

## Usage

1. Clone or download the project to your local machine.

2. Navigate to the project directory using your terminal.

3. Run the script with the following command, providing the desired database name as an argument:

   ```bash
   python db_operations.py <database_name>
   ```

   Replace `<database_name>` with your preferred name for the MongoDB database.

4. The script will read all the CSV files located in the "data" directory and insert their data into the specified MongoDB database as timeseries collections. Each CSV file will become a separate collection, and the "Date" column in the CSV files will be converted to MongoDB's datetime format.

5. Once the script finishes running, your data will be available in the specified MongoDB database for further analysis and querying.

## Directory Structure

The directory structure for this project should look like this:

```
project_name/
│
├── data/
│   ├── crypto1.csv
│   ├── crypto2.csv
│   └── ...
│
├── db/
│   ├── db_operations.py
│   ├── ...
│
├── ...
```

Ensure that your CSV files are placed inside the "data" directory before running the script.

## Configuration

You may need to adjust the MongoDB connection URI in the script to match your specific MongoDB setup. Modify the following line in `db_operations.py`:

```python
client = MongoClient("mongodb://localhost:27017/")
```

Replace `"mongodb://localhost:27017/"` with your MongoDB connection URI.

Make sure mongoDB server is running on your local machine