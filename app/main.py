from bson.tz_util import FixedOffset
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, g
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import sys

app = Flask(__name__)

def get_mongo_client(database_name):
    # Modify the connection string to include the database name from the command line
    return MongoClient(f"mongodb://localhost:27017/{database_name}")

@app.teardown_request
def teardown_mongo_client(exception):
    if hasattr(g, 'mongo_client'):
        g.mongo_client.close()

@app.route('/get_data', methods=['GET'])
def get_data():

    """
    Get time series data within a specified date range.

    Args:
        collection_name (str): The name of the MongoDB collection.
        start_date_str (str): The start date in ISO 8601 format.
        end_date_str (str): The end date in ISO 8601 format.

    Returns:
        json: JSON response containing time series data.
    """
    
    try:
        collection_name = request.args.get('collection_name')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        mongo_client = g.mongo_client = get_mongo_client(app.config['DATABASE_NAME'])
        collection = mongo_client[app.config['DATABASE_NAME']][collection_name]


        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=FixedOffset(0, "Z"))
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=FixedOffset(0, "Z"))

        query = {"Date": {"$gte": start_date, "$lte": end_date}}

        cursor = collection.find(query)
        result = []

        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)

        return jsonify(result)
    except ValueError as ve:
        return jsonify({"error": "Invalid date format. Please use ISO 8601 format: %Y-%m-%dT%H:%M:%S.%fZ"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trend', methods=['GET'])
def calculate_trend():

        """
    Calculate the trend based on the Simple Moving Average (SMA) of the 'Open' column.

    Args:
        collection_name (str): The name of the MongoDB collection.
        window_str (str): The time window for calculating the trend (e.g., '7d', '24h', '60m').

    Returns:
        json: JSON response containing data points and trend.
    """

    try:
        collection_name = request.args.get('collection_name')
        window_str = request.args.get('window')

        mongo_client = g.mongo_client = get_mongo_client(app.config['DATABASE_NAME'])
        collection = mongo_client[app.config['DATABASE_NAME']][collection_name]


        # Calculate the start and end times for the time window
        duration = int(window_str[:-1])
        period = window_str[-1]

        if period == 'd':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=duration)
        elif period == 'h':
            end_date = datetime.now()
            start_date = end_date - timedelta(hours=duration)
        elif period == 'm':
            # Check if the requested window is valid for the available data
            if duration < 1440:  # 1440 minutes in a day
                return jsonify({"error": "Invalid 'window' parameter for minute-level data."}), 400
            end_date = datetime.now()
            start_date = end_date - timedelta(minutes=duration)
        else:
            return jsonify({"error": "Invalid period indicator in 'window' parameter. Use 'd', 'h', or 'm'."}), 400

        query = {"Date": {"$gte": start_date, "$lte": end_date}}

        cursor = collection.find(query)
        df = pd.DataFrame(list(cursor))

        if df.empty:
            return jsonify({"error": "No data available for the requested time period."}), 400

        # Calculate the Simple Moving Average (SMA) of the 'Open' column
        if 'Open' not in df.columns:
            return jsonify({"error": "No 'Open' column found in the data."}), 400

        sma = df['Open'].mean()

        # Determine the trend based on SMA
        if sma > df['Open'].iloc[-1]:
            trend = "decrease"
        elif sma < df['Open'].iloc[-1]:
            trend = "increase"
        else:
            trend = "stable"

        response_data = {
            "dataPoints": len(df),  # Return the actual count of data points within the specified time window
            "trend": trend
        }

        return jsonify(response_data)
    except ValueError as ve:
        return jsonify({"error": "Invalid parameter format."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <database_name>")
        sys.exit(1)

    database_name = sys.argv[1]  # Get the database name from the command-line argument

    app.config['DATABASE_NAME'] = database_name  # Store the database name in the Flask app config
    app.run(debug=True)