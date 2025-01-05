import boto3
from click import echo

class Config:
    def __init__(self, name: str, region: str = None):
        self.name = name
        session = boto3.session.Session()
        self.region = session.region_name if not region else region
        self.sts_client = boto3.client("sts")

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def get_account_id(self):
        try:
            return self.sts_client.get_caller_identity()["Account"]
        except Exception as e:
            echo(f"Error fetching account ID: {e}")
            return None

    def get_tags(self, owner: bool=False) -> list:
        v2_tags = self.get_v2_tags(owner)
        return [{'Key': k, 'Value': v} for k, v in v2_tags.items()]
    
    def get_v2_tags(self, owner: bool=False) -> list:
        tags = {'AppName': self.name}
        if owner:
            tags['Owner'] = 'kobidh'
        else:
            tags['Publisher'] = 'kobidh'
        return tags