import boto3
from time import sleep
from botocore.exceptions import ClientError
from .aws import AWS
from utils.logging import log, log_error, log_warning


class DynamoDB(AWS):
    """
        Handles platform configuration details
    """

    def __init__(self, table_name, keys):
        session = boto3.session.Session()
        self.dynamodb = session.resource('dynamodb')
        self.dynamodb_client = session.client('dynamodb')
        self.keys = keys
        self.table_name = table_name
        self.table = self._get_or_create()

    def _get_or_create(self):
        try:
            self.dynamodb_client.describe_table(TableName=self.table_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                log_warning(
                    f"Table {self.table_name} not found, creating one ...")
                self._create()
            else:
                log_error(f"An unexpected error occurred: {e}")
        return self.dynamodb.Table(self.table_name)

    def _creation_status(self):
        status = ""
        while status != "ACTIVE":
            log(f"\rChecking {self.table_name} table creation status...", nl=False)
            sleep(2)
            status = self.dynamodb_client.describe_table(
                TableName=self.table_name)["Table"]["TableStatus"]
        log(f"\r{self.table_name} table status is ACTIVE                ")

    def _create(self):
        key_schema = [
            {'AttributeName': self.keys[0], 'KeyType': 'HASH'}]
        key_schema.extend([{'AttributeName': key, 'KeyType': 'RANGE'}
                          for key in self.keys[1:]])
        self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=key_schema,
            AttributeDefinitions=[
                {'AttributeName': key, 'AttributeType': 'S'} for key in self.keys],
            BillingMode='PAY_PER_REQUEST',
            Tags=self.get_tags(self.table_name, owner=True)
        )
        self._creation_status()

    def get(self):
        return self.table

    def _deletion_status(self):
        pass

    def delete(self):
        pass
