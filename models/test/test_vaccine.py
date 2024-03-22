import unittest
from models.test.vaccine import Vaccine

class VaccineTestCase(unittest.TestCase):
    def setUp(self):
        self.vaccine = Vaccine(
            names="COVID-19",
            no_doses=2
        )

    def test_vaccine_attributes(self):
        self.assertEqual(self.vaccine.names, "COVID-19")
        self.assertEqual(self.vaccine.no_doses, 2)

    def test_vaccine_initialization(self):
        self.assertIsInstance(self.vaccine, Vaccine)

if __name__ == "__main__":
    unittest.main()