import json
from meta import VERSION
from click import confirm, echo
from services.config import Config
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
            self.kobidh_version = VERSION
            self.vpc = VPCConfig(name, region)
            self.ecs = ECSConfig(name, region)
        
        def __eq__(self, other: object) -> bool:
            if isinstance(other, EnvironmentConfig.Template):
                return (self.name == other.name and self.region == other.region and self.kobidh_version == other.kobidh_version
                        and self.vpc == other.vpc and self.ecs == other.ecs)
            return False

        def __ne__(self, other: object) -> bool:
            return not self.__eq__(other)
        
        def json(self):
            self.vpc = self.vpc.json()
            self.ecs = self.ecs.json()
            return {
                "name": self.name,
                "region": self.region,
                "vpc": self.vpc,
                "ecs": self.ecs
            }
        
        def parse_json(self, json_data: dict):
            """
            Deserialize a JSON string into an EnvironmentConfig.Template object.

            :param json_data: JSON string to deserialize.
            """
            if not json_data:
                return
            self.kobidh_version = json_data.get("kobidh_version", None)
            self.vpc = VPCConfig(self.name, self.region)
            self.vpc.parse_json(json_data.get("vpc", None))
            self.ecs = ECSConfig(self.name, self.region)
            self.ecs.parse_json(json_data.get("ecs", None))
    
    def __init__(self, name: str, region: str=None):
        super().__init__(name, region)
        self.table = DynamoDB(ENVIRONMENT_CONFIG_TABLE, ['environment']).get()
        self.config = EnvironmentConfig.Template(self.name, self.region)

    def _compare(self, record):
        configuration = record["configuration"]
        env_config = EnvironmentConfig.Template(self.name, self.region)
        env_config.parse_json(configuration)
        return self.config != env_config

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

        configuration = record["configuration"]
        env_config = EnvironmentConfig.Template(self.name, self.region)
        env_config.parse_json(configuration)
        # the following confirm will be prompted when the CONFIGURATION mismatches
        if self.config != env_config and confirm('Do you want to update the environment config?'):
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
