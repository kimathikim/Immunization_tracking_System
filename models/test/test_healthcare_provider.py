import unittest
from models.test.healthcare_provider import Practitioner

class PractitionerTestCase(unittest.TestCase):
    def setUp(self):
        self.practitioner = Practitioner(
            first_name="John",
            second_Name="Doe",
            email="john.doe@example.com",
            phone_number=1234567890,
            password="password123"
        )

    def test_practitioner_attributes(self):
        self.assertEqual(self.practitioner.first_name, "John")
        self.assertEqual(self.practitioner.second_Name, "Doe")
        self.assertEqual(self.practitioner.email, "john.doe@example.com")
        self.assertEqual(self.practitioner.phone_number, 1234567890)
        self.assertEqual(self.practitioner.password, "password123")

    def test_practitioner_initialization(self):
        self.assertIsInstance(self.practitioner, Practitioner)

    def test_is_active_property(self):
        self.assertTrue(self.practitioner.is_active)

    def test_is_authenticated_property(self):
        self.assertTrue(self.practitioner.is_authenticated)

    def test_get_id_method(self):
        self.assertEqual(self.practitioner.get_id(), "john.doe@example.com")

if __name__ == "__main__":
    unittest.main()