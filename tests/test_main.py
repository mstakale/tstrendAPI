import unittest
import json
import sys
from os.path import abspath, dirname

# Add the path to the parent directory of 'app' to the system path
sys.path.append(abspath(dirname(dirname(__file__))))

from app.main import app  # Assuming your Flask app is in app/main.py

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_data_valid(self):
        response = self.app.get('/get_data?collection_name=your_collection&start_date=2023-01-01T00:00:00.000Z&end_date=2023-01-02T00:00:00.000Z')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_get_data_invalid_date_format(self):
        response = self.app.get('/get_data?collection_name=your_collection&start_date=invalid_date_format&end_date=2023-01-02T00:00:00.000Z')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_calculate_trend_valid(self):
        response = self.app.get('/trend?collection_name=your_collection&window=7d')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('dataPoints' in data)
        self.assertTrue('trend' in data)

    def test_calculate_trend_invalid_period(self):
        response = self.app.get('/trend?collection_name=your_collection&window=7x')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_not_found_error(self):
        response = self.app.get('/nonexistent_endpoint')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not Found')

if __name__ == '__main__':
    unittest.main()
