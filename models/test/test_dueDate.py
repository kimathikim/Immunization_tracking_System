import unittest
from models.test.dueDate import Duedate

class DuedateTestCase(unittest.TestCase):
    def setUp(self):
        self.duedate = Duedate(
            due_date="2022-01-01",
            vaccine_administration_id="123456789"
        )

    def test_duedate_attributes(self):
        self.assertEqual(self.duedate.due_date, "2022-01-01")
        self.assertEqual(self.duedate.vaccine_administration_id, "123456789")

    def test_duedate_initialization(self):
        self.assertIsInstance(self.duedate, Duedate)

if __name__ == "__main__":
    unittest.main()