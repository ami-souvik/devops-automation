import json
from meta import VERSION
from click import confirm, echo
from utils.logging import log, log_list
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
        
        def __dir__(self):
            return ['name', 'region', 'kobidh_version', 'vpc', 'ecs']
        
        def __eq__(self, other: 'EnvironmentConfig.Template') -> bool:
            return (self.name == other.name and self.region == other.region and self.kobidh_version == other.kobidh_version and
                self.vpc == other.vpc and self.ecs == other.ecs)

        def __ne__(self, other: object) -> bool:
            return not self.__eq__(other)
        
        def compare_logs(self, other: 'EnvironmentConfig.Template') -> list[tuple]:
            level = 0
            logs = []
            logs.append(("# Environment Configuration", 'blue', level))
            logs.append(("{", 'white', level))
            object_logs = []
            for attr in dir(other):
                if getattr(other, attr) != getattr(self, attr):
                    if attr == 'vpc':
                        object_logs.extend(self.vpc.compare_logs(other.vpc, level=1))
                    elif attr == 'ecs':
                        object_logs.extend(self.ecs.compare_logs(other.ecs, level=1))
                    else:
                        logs.append((f"{attr}: {getattr(other, attr)} -> {getattr(self, attr)}", 'yellow', level+1))
            logs.extend(object_logs)
            logs.append(("}\n", 'white', level))
            log_list(logs)

        
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
        echo("Comparing environment_configs:")
        if self.config != env_config:
            self.config.compare_logs(env_config)
            return True
        log("Configurations Matched")
        return False

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
