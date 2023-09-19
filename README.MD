
```markdown
# Crypto Time Series API

Crypto Time Series API is a Flask-based web service that provides cryptocurrency time series data within a specified time range 
and trend information for a given window in time series data. 
This API is designed to help users analyze and visualize cryptocurrency market trends.

## Getting Started

These instructions will guide you through setting up and running the Crypto Time Series API locally. 
Ensure you have Python and MongoDB installed on your system before proceeding.

### Prerequisites

- Python 3.8.x
- MongoDB

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone git@github.com:mstakale/tstrendAPI.git
   ```

2. Navigate to the project directory:

   ```bash
   cd tstrendAPI
   ```

3. Install the required Python dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

To store cryptocurrency time series data, you need to set up a MongoDB database. Follow these steps:

1. Start your MongoDB server.

2. Create a new MongoDB database by running the following command in the project directory:

   ```bash
   python db/db_operations.py your-database-name
   ```

### Usage

Run the Flask API using the following command:

- Using `main.py` with database name as a command-line argument:

   ```bash
   python main.py your-database-name
   ```

- Using `app.py` (database name is set in the code):

   ```bash
   python app.py
   ```

**Access the API**:

   Once the API is running, you can access it using the provided endpoints (see below).

## API Endpoints

### 1. Retrieve Time Series Data

- **Endpoint**: `/get_data`
- **Method**: GET

**Parameters**:
- `collection_name` (string): The name of the data collection in the database.
- `start_date` (string, ISO 8601 format): The start date for data retrieval.
- `end_date` (string, ISO 8601 format): The end date for data retrieval.

### 2. Calculate Data Trend

- **Endpoint**: `/trend`
- **Method**: GET

**Parameters**:
- `collection_name` (string): The name of the data collection in the database.
- `window` (string): The time window for trend calculation (e.g., '7d' for 7 days, '24h' for 24 hours, '60m' for 60 minutes).


```http
GET http://127.0.0.1:5000/trend?collection_name=BNB&window=7d
GET http://127.0.0.1:5000/get_data?collection_name=BTC&start_date=2015-04-02T23:59:59.000Z&end_date=2015-04-04T23:59:59.000Z
```

### Running Tests

Unit tests for the API are located in the `tests` directory. To run the tests, use the following command:

```bash
python -m unittest tests/test_main.py
```

## Directory Structure

- `data/`: Contains cryptocurrency time series data files.
- `db/`: Includes database setup and operations (MongoDB).
- `app/`: Holds the Flask API code.
- `tests/`: Contains unit tests for the API.
- `requirements.txt`: Lists the project dependencies.

## Dependencies

- Flask: Web framework for building the API.
- pymongo: MongoDB driver for Python.

## Contributing

If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature/bugfix.
3. Make your changes and commit them with clear, concise messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.


## Contact

If you have any questions or feedback, feel free to contact the project maintainers:

- Manisha Takale (manishatakale@gmail.com)

```
