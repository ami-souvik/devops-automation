from resources.vpc import VPC
from services.config.env_config import EnvironmentConfig

class Environment:

    def __init__(self, name: str, region: str):
        self.env_config = EnvironmentConfig(name, region)
        self.vpc_handler = VPC(self.env_config)
        pass

    def describe(self):
        self.vpc_handler.describe()

    def create(self):
        self.env_config.setup()
        self.vpc_handler.run()
        pass

    def update(self):
        pass

    def delete(self):
        self.env_config.delete()
        self.vpc_handler.run()
