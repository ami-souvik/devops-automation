import json

class AppDescribe:
    def __init__(self, name, apigateway, ecr): 
        self.name = name
        self.apigateway = apigateway
        self.ecr = ecr

    def serialize(self):
        return json.dumps(self.__dict__, indent=2, sort_keys=True, default=str)
