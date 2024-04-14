import unittest
import json
from server import app 

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_put(self):
        data = {'key': 'test_key', 'value': 'test_value'}
        response = self.app.post('/put', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'message', response.data)

    def test_get(self):
        response = self.app.get('/get?key=test_key')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value', response.data)

    def test_get_all_keys(self):
        response = self.app.get('/getall')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data.decode('utf-8')), list)

    def test_delete(self):
        response = self.app.delete('/delete?key=test_key')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted', response.data)

    def test_update(self):
        data = {'key': 'test_key', 'value': 'updated_value'}
        response = self.app.put('/update', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'message', response.data)

if __name__ == '__main__':
    unittest.main()
