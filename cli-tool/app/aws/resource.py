import boto3

class AWSResource:
    def __init__(self, resource: str, region: str = None):
        sts_client = boto3.client('sts')
        self.account_id = sts_client.get_caller_identity()['Account']
    
        self.region = region
        self.client = boto3.client(resource, region_name=region)

    def get_tags(self, name: str) -> list:
        v2_tags = self.get_v2_tags(name)
        return [{'Key': k, 'Value': v} for k, v in v2_tags.items()]
    
    def get_v2_tags(self, name: str) -> list:
        return {
            'publisher': 'kobidh',
            'name': name
        }
