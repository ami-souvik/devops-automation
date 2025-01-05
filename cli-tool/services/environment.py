from resources.vpc import VPC
from resources.ecs import ECS
from services.config.env_config import EnvironmentConfig

class Environment:

    def __init__(self, name: str, region: str):
        self.env_config = EnvironmentConfig(name, region)
        self.vpc_handler = VPC(self.env_config)
        self.ecs_handler = ECS(self.env_config)
        pass

    def describe(self):
        self.env_config.setup()
        # self.ecs_handler.run()

    def create(self):
        self.env_config.setup()
        self.vpc_handler.run()
        pass

    def update(self):
        pass

    def delete(self):
        self.env_config.delete()
        self.vpc_handler.run()
