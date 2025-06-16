import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    @patch('app.mysql.connector.connect', return_value=MagicMock(cursor=lambda:>
    def test_post(self, _):
        r = app.test_client().post("/data", json={
            "plant_id":1,"timestamp":"2025-06-01T12:00",
            "temperature_celsius":23.5,"humidity_percent":45.2,
            "soil_moisture_percent":28.4,"light_lux":650
        })
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
