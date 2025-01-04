import boto3

class AWS:
    def __init__(self, region: str = None):
        session = boto3.session.Session()
        self.region = session.region_name if not region else region

    def get_tags(self, name: str, owner: bool=False) -> list:
        v2_tags = self.get_v2_tags(name, owner)
        return [{'Key': k, 'Value': v} for k, v in v2_tags.items()]
    
    def get_v2_tags(self, name: str, owner: bool=False) -> list:
        tags = {'name': name}
        if owner:
            tags['owner'] = 'kobidh'
        else:
            tags['publisher'] = 'kobidh'
        return tags
