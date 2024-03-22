import unittest
from models.test.child import Child

class ChildTestCase(unittest.TestCase):
    def setUp(self):
        self.child = Child(
            first_name="Alice",
            second_name="Smith",
            date_of_birth="2000-01-01",
            parent_id="123456789"
        )

    def test_child_attributes(self):
        self.assertEqual(self.child.first_name, "Alice")
        self.assertEqual(self.child.second_name, "Smith")
        self.assertEqual(self.child.date_of_birth, "2000-01-01")
        self.assertEqual(self.child.parent_id, "123456789")

    def test_child_initialization(self):
        self.assertIsInstance(self.child, Child)

if __name__ == "__main__":
    unittest.main()