import unittest
from models.test.sessionManager import Session

class SessionTestCase(unittest.TestCase):
    def setUp(self):
        self.session = Session(
            email="test@example.com",
            expiration_time=datetime.utcnow() + timedelta(minutes=30)
        )

    def test_session_attributes(self):
        self.assertEqual(self.session.email, "test@example.com")
        self.assertEqual(self.session.expiration_time, datetime.utcnow() + timedelta(minutes=30))

    def test_session_initialization(self):
        self.assertIsInstance(self.session, Session)

if __name__ == "__main__":
    unittest.main()