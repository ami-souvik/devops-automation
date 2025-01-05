import boto3

class Config:
    def __init__(self, name: str, region: str = None):
        self.name = name
        session = boto3.session.Session()
        self.region = session.region_name if not region else region

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def get_tags(self, name: str, owner: bool=False) -> list:
        v2_tags = self.get_v2_tags(name, owner)
        return [{'Key': k, 'Value': v} for k, v in v2_tags.items()]
    
    def get_v2_tags(self, name: str, owner: bool=False) -> list:
        tags = {'Name': name}
        if owner:
            tags['Owner'] = 'kobidh'
        else:
            tags['Publisher'] = 'kobidh'
        return tags