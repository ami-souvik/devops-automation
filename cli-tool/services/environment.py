from services.config.env_config import EnvironmentConfig

class Environment:

    def __init__(self, name: str):
        self.name = name
        EnvironmentConfig()
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
