import unittest
from models.test.vaccineAdministration import Vaccine_administration

class VaccineAdministrationTestCase(unittest.TestCase):
    def setUp(self):
        self.vaccine_administration = Vaccine_administration(
            administration_date="2022-01-01",
            confirmation_status="Confirmed",
            practitioner_name="Dr. John Doe",
            child_id="123456789",
            vaccine_id="987654321",
            practitioner_id="567890123"
        )

    def test_vaccine_administration_attributes(self):
        self.assertEqual(self.vaccine_administration.administration_date, "2022-01-01")
        self.assertEqual(self.vaccine_administration.confirmation_status, "Confirmed")
        self.assertEqual(self.vaccine_administration.practitioner_name, "Dr. John Doe")
        self.assertEqual(self.vaccine_administration.child_id, "123456789")
        self.assertEqual(self.vaccine_administration.vaccine_id, "987654321")
        self.assertEqual(self.vaccine_administration.practitioner_id, "567890123")

    def test_vaccine_administration_initialization(self):
        self.assertIsInstance(self.vaccine_administration, Vaccine_administration)

if __name__ == "__main__":
    unittest.main()