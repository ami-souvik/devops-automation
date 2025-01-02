from resources.dynamodb import DynamoDB

ENVIRONMENT_CONFIG_TABLE = 'environment_configs'


class EnvironmentConfig:
    """
        Contains environment configuration details
    """
    def __init__(self, name: str=None):
        self.environment = name
        self.table = DynamoDB(ENVIRONMENT_CONFIG_TABLE, [('environment', self.environment)])
