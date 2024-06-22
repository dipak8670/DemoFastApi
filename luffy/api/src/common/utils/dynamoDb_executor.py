import boto3


class DynamoDbExecutor:
    def __init__(self):
        self.dynamodb_resource = boto3.resource("dynamodb")
        self.__table = self.dynamodb_resource.Table("STUDENT")

    def save(self, item: dict):
        try:
            return self.__table.put_item(Item=item)
        except Exception as e:
            print(e)
            raise e

    def get(self, key):
        try:
            return self.__table.get_item(Key=key)
        except Exception as e:
            print(e)
            raise e
