from resources.vpc import VPC
from resources.ecs import ECS
from services.config.env_config import EnvironmentConfig

class Environment:

    def __init__(self, name: str, region: str=None):
        self.env_config = EnvironmentConfig(name, region)
        self.vpc_handler = VPC(self.env_config)
        self.ecs_handler = ECS(self.env_config)
        pass

    def describe(self):
        self.env_config.setup()

    def create(self):
        self.env_config.setup()
        self.vpc_handler.run()
        self.ecs_handler.run()
        pass

    def update(self):
        pass

    def delete(self):
        self.env_config.delete()
        self.vpc_handler.run()
        self.ecs_handler.run()

    def configure(self):
        self.vpc_handler.configure()
        self.vpc_handler.apply()
