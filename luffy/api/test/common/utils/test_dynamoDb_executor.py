import unittest
from unittest.mock import patch, MagicMock
from luffy.api.src.common.utils.dynamoDb_executor import DynamoDbExecutor


class TestDynamoDbExecutor(unittest.TestCase):
    @patch("boto3.resource")
    def setUp(self, mock_boto_resource):
        self.mock_dynamodb = MagicMock()
        self.mock_table = MagicMock()
        mock_boto_resource.return_value = self.mock_dynamodb
        self.mock_dynamodb.Table.return_value = self.mock_table
        self.executor = DynamoDbExecutor()

    def test_save_item(self):
        self.mock_table.put_item.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 200}
        }
        item = {"id": "1", "name": "John Doe"}
        response = self.executor.save(item)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.mock_table.put_item.assert_called_once_with(Item=item)

    def test_get_item(self):
        item = {"id": "1", "name": "John Doe"}
        self.mock_table.get_item.return_value = {"Item": item}
        response = self.executor.get({"id": "1"})
        self.assertIn("Item", response)
        self.assertEqual(response["Item"], item)
        self.mock_table.get_item.assert_called_once_with(Key={"id": "1"})

    def test_save_item_exception(self):
        self.mock_table.put_item.side_effect = Exception("Error saving item")
        with self.assertRaises(Exception) as context:
            self.executor.save({"id": "2", "name": "Jane Doe"})
        self.assertEqual(str(context.exception), "Error saving item")
        self.mock_table.put_item.assert_called_once_with(
            Item={"id": "2", "name": "Jane Doe"}
        )

    def test_get_item_exception(self):
        self.mock_table.get_item.side_effect = Exception("Error getting item")
        with self.assertRaises(Exception) as context:
            self.executor.get({"id": "2"})
        self.assertEqual(str(context.exception), "Error getting item")
        self.mock_table.get_item.assert_called_once_with(Key={"id": "2"})
