import boto3

from luffy.api.src.common.enum.aws_enum import AwsEnum


class DynamoDbExecutor:
    def __init__(self):
        aws = {
            "aws_access_key_id" : AwsEnum.ACCESS_KEY_ID.value,
            "aws_secret_access_key" : AwsEnum.ACCESS_KEY.value,
            "region_name":"us-west-2"
        }
        self.dynamodb_resource = boto3.resource(
            "dynamodb",
            region_name=aws["region_name"],
            aws_access_key_id=aws["aws_access_key_id"],
            aws_secret_access_key=aws["aws_secret_access_key"],
        )
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
