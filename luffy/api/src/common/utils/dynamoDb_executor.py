import boto3
import logging


class DynamoDbExecutor:
    def __init__(self):
        self.dynamodb_resource = boto3.resource("dynamodb")
        self.__table = self.dynamodb_resource.Table("StudentApiDynamoDBTable")

    def save(self, item: dict):
        try:
            return self.__table.put_item(Item=item)
        except Exception as e:
            logging.error(e)
            raise e

    def get(self, key):
        try:
            return self.__table.get_item(Key=key)
        except Exception as e:
            logging.error(e)
            raise e
