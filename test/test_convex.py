import sys
import os 
import unittest
from unittest.mock import MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.convex import Convex

class ConvexTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'http://localhost:3001/'
        self.convex = Convex(self.base_url)

    def test_create_user(self):
        excepted_response = {
            "id": "1",
        }

        requests = MagicMock()

        requests.post.return_value.json.return_value = excepted_response

        sys.modules['requests'] = requests

        response = self.convex.create_user("John Doe")
        self.assertEqual(response.content, excepted_response)


if __name__ == '__main__':
    unittest.main()