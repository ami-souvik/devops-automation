import boto3
from utilities.env_handler import get_env_vars


class Boto3Manager:
    def __init__(self) -> None:
        self.session = boto3.Session(
            aws_access_key_id=get_env_vars("aws_access_key"),
            aws_secret_access_key=get_env_vars("aws_access_secret"),
            region_name=get_env_vars("region")
        )

    def get_client(self, service):
        try:
            self.session.client(service)
        except Exception as e:
            print(e)
