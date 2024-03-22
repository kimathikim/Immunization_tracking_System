import unittest
from models.test.hospitals import Hospital

class HospitalTestCase(unittest.TestCase):
    def setUp(self):
        self.hospital = Hospital(
            name="St. Mary's Hospital",
            location="New York"
        )

    def test_hospital_attributes(self):
        self.assertEqual(self.hospital.name, "St. Mary's Hospital")
        self.assertEqual(self.hospital.location, "New York")

    def test_hospital_initialization(self):
        self.assertIsInstance(self.hospital, Hospital)

if __name__ == "__main__":
    unittest.main()