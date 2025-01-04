import json
from meta import VERSION
from click import confirm, echo
from services.config.config import Config
from services.config.vpc_config import VPCConfig
from services.config.ecs_config import ECSConfig
from resources.dynamodb import DynamoDB

ENVIRONMENT_CONFIG_TABLE = 'environment_configs'


class EnvironmentConfig(Config):
    """
        Contains environment configuration details
    """
    class Template:
        def __init__(self, name: str, region: str):
            self.name = name
            self.region = region
            self.vpc = VPCConfig(name, region)
        
        def __eq__(self, other):
            if isinstance(other, EnvironmentConfig.Template):
                return (self.name == other.name and self.region == other.region and self.vpc == other.vpc)
            return False

        def json(self):
            self.vpc = self.vpc.json()
            return {
                "name": self.name,
                "region": self.region,
                "vpc": self.vpc
            }
    
    def __init__(self, name: str, region: str=None):
        super().__init__(name, region)
        self.table = DynamoDB(ENVIRONMENT_CONFIG_TABLE, ['environment']).get()
        self.config = EnvironmentConfig.Template(self.name, self.region)

    def _compare(self, record):
        configuration = record["configuration"]
        if configuration.get("kobidh_version", None) != VERSION:
            return True
        vpc = configuration["vpc"]
        vpc_config = VPCConfig(self.name, self.region)
        vpc_config.parse_json(vpc)
        return not self.config.vpc == vpc_config

    def _configure(self):
        pass

    def get(self):
        response = self.table.get_item(
            Key={
                'environment': self.config.name
            },
            ConsistentRead=True,
            AttributesToGet=[
                'configuration'
            ]
        )
        return response.get('Item', None)

    def _update(self):
        config = self.config.json()
        config['kobidh_version'] = VERSION
        return self.table.update_item(
            TableName=ENVIRONMENT_CONFIG_TABLE,
            Key={
                'environment': self.config.name
            },
            UpdateExpression='SET configuration = :configuration',
            ExpressionAttributeValues={
                ':configuration': config
            },
            ReturnValues="UPDATED_NEW"
        )

    def _get_or_create(self):
        record = self.get()
        if not record:
            self._configure()
            self._update()
        # the following confirm will be prompted when the CONFIGURATION mismatches
        elif self._compare(record) and confirm('Do you want to update the environment config?'):
            record = self._update()
        return record

    def setup(self):
        return self._get_or_create()
    
    def delete(self):
        return self.table.delete_item(
            Key={
                'environment': self.config.name
            }
        )
