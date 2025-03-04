import boto3

class AWSResource:
    def __init__(self, resource: str, region: str = None):
        self.region = region
        self.client = boto3.client(resource, region_name=region)

    def get_tags(self, name: str) -> list:
        v2_tags = self.get_v2_tags(name)
        return [{'Key': k, 'Value': v} for k, v in v2_tags.items()]
    
    def get_v2_tags(self, name: str) -> list:
        return {
            'Publisher': 'kobidh',
            'Name': name
        }
