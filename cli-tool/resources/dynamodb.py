import boto3
from time import sleep
from botocore.exceptions import ClientError
from .aws import AWS
from utils.logging import log, log_error, log_warning

class DynamoDB(AWS):
    """
        Handles platform configuration details
    """
    def __init__(self, table_name, kv_pairs):
        session = boto3.session.Session()
        self.dynamodb = session.resource('dynamodb')
        self.dynamodb_client = session.client('dynamodb')
        self.kv_pairs = kv_pairs
        self.table_name = table_name
        self.get_or_create_table()

    def get_or_create_table(self):
        try:
            self.dynamodb_client.describe_table(TableName=self.table_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                log_warning(f"Table {self.table_name} not found, creating one ...")
                self.create_table()
            else:
                log_error(f"An unexpected error occurred: {e}")
        return self.dynamodb.Table(self.table_name)
    
    def create_table(self):
        key_schema = [
            {'AttributeName': self.kv_pairs[0][0], 'KeyType': 'HASH'}]
        key_schema.extend([{'AttributeName': key, 'KeyType': 'RANGE'} for key, _ in self.kv_pairs[1:]])
        self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=key_schema,
            AttributeDefinitions=[
                {'AttributeName': key, 'AttributeType': 'S'} for key, _ in self.kv_pairs],
            BillingMode='PAY_PER_REQUEST',
            Tags=self.get_tags(self.table_name, owner=True)
        )
        self.table_creation_status()

    def table_creation_status(self):
        status = ""
        while status != "ACTIVE":
            log(f"\rChecking {self.table_name} table creation status...", nl=False)
            sleep(2)
            status = self.dynamodb_client.describe_table(
                TableName=self.table_name)["Table"]["TableStatus"]
        log(f"\r{self.table_name} table status is ACTIVE                ")
    
    def delete_table(self):
        pass

    def table_deletion_status(self):
        pass