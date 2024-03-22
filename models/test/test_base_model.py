import unittest
from models.test.base_model import BaseModel

class BaseModelTestCase(unittest.TestCase):
    def setUp(self):
        self.base_model = BaseModel(
            id="123",
            Created_at="2022-01-01 00:00:00",
            Updated_at="2022-01-01 00:00:00"
        )

    def test_base_model_attributes(self):
        self.assertEqual(self.base_model.id, "123")
        self.assertEqual(self.base_model.Created_at, "2022-01-01 00:00:00")
        self.assertEqual(self.base_model.Updated_at, "2022-01-01 00:00:00")

    def test_base_model_initialization(self):
        self.assertIsInstance(self.base_model, BaseModel)

    def test_base_model_to_dict(self):
        expected_dict = {
            "id": "123",
            "Created_at": "2022-01-01 00:00:00",
            "Updated_at": "2022-01-01 00:00:00",
            "__class__": "BaseModel"
        }
        self.assertEqual(self.base_model.to_dict(), expected_dict)

    def test_base_model_save(self):
        # TODO: Implement test for save method
        pass

    # def test_base_model_delete(self):
    #     # TODO: Implement test for delete method
    #     pass

if __name__ == "__main__":
    unittest.main()