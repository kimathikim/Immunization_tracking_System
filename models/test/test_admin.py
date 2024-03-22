import unittest
from models.test.admin import Admin

class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.admin = Admin(
            first_name="John",
            second_Name="Doe",
            email="john.doe@example.com",
            phone_number=1234567890,
            password="password123",
            id_No="123456789",
            reset_token="token123",
            profile_picture="profile.jpg",
            token_expiration="2022-01-01 00:00:00",
            alternative_id="alt_id"
        )

    def test_admin_attributes(self):
        self.assertEqual(self.admin.first_name, "John")
        self.assertEqual(self.admin.second_Name, "Doe")
        self.assertEqual(self.admin.email, "john.doe@example.com")
        self.assertEqual(self.admin.phone_number, 1234567890)
        self.assertEqual(self.admin.password, "password123")
        self.assertEqual(self.admin.id_No, "123456789")
        self.assertEqual(self.admin.reset_token, "token123")
        self.assertEqual(self.admin.profile_picture, "profile.jpg")
        self.assertEqual(self.admin.token_expiration, "2022-01-01 00:00:00")
        self.assertEqual(self.admin.alternative_id, "alt_id")

    def test_admin_initialization(self):
        self.assertIsInstance(self.admin, Admin)

if __name__ == "__main__":
    unittest.main()