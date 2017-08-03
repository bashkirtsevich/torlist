import unittest
from torlist_server import app
import json


class TestCase(unittest.TestCase):
    def test_index(self):
        with app.test_client() as client:
            response = client.get('/')

            self.assertEqual(response.status_code, 200, "Wrong response code")
            self.assertEqual(response.content_type, "application/json", "Wrong content type")
            self.assertIsNotNone(response.data, "Empty response data")

            r_dict = json.loads(response.data.decode("utf-8"))
            self.assertTrue(isinstance(r_dict, dict), "Invalid JSON response type")

    def test_get_last_update(self):
        with app.test_client() as client:
            response = client.get('/get_last_update')
            self.assertEqual(response.status_code, 200, "Wrong response code")
            self.assertEqual(response.content_type, "application/json", "Wrong content type")
            self.assertIsNotNone(response.data, "Empty response data")

            r_dict = json.loads(response.data.decode("utf-8"))
            self.assertTrue(isinstance(r_dict, dict), "Invalid JSON response type")
            self.assertTrue("result" in r_dict, "Missed 'result' dict in JSON response")
            self.assertTrue(isinstance(r_dict["result"], str), "Invalid result type")

    def test_is_contains_ip(self):
        with app.test_client() as client:
            response = client.get('/is_contains_ip/ub2435ierug39')
            self.assertEqual(response.status_code, 200, "Wrong response code")
            self.assertEqual(response.content_type, "application/json", "Wrong content type")
            self.assertIsNotNone(response.data, "Empty response data")

            r_dict = json.loads(response.data.decode("utf-8"))
            self.assertTrue(isinstance(r_dict, dict), "Invalid JSON response type")
            self.assertTrue("result" in r_dict, "Missed 'result' dict in JSON response")
            self.assertTrue(isinstance(r_dict["result"], bool), "Invalid result type")
            self.assertTrue(r_dict["result"] == False, "Invalid result value")


if __name__ == '__main__':
    unittest.main()
