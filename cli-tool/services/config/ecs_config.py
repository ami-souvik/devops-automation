from services.config import Config

class ECSConfig(Config):
    """
        Contains ECS configuration details
    """
    def __init__(self, name: str, region: str):
        self.name = name
        self.region = region
        self.cluster_arn = None
        self.cluster_name = f"{name}-cluster"

    def __dir__(self):
        return ['cluster_arn', 'cluster_name']

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ECSConfig):
            return (self.cluster_arn == other.cluster_arn and self.cluster_name == other.cluster_name)
        return False

    def compare_logs(self, other: 'ECSConfig', level=0) -> bool:
        logs = []
        logs.append(("# ECS Configuration", 'blue', level))
        logs.append(("{", 'white', level))
        for attr in dir(self):
            if getattr(other, attr) != getattr(self, attr):
                logs.append((f"{attr}: {getattr(other, attr)} -> {getattr(self, attr)}", 'yellow', level+1))
        logs.append(("}", 'white', level))
        return logs

    def json(self):
        return {
            "cluster_arn": self.cluster_arn,
            "cluster_name": self.cluster_name
        }
    
    def parse_json(self, json_data: dict):
        """
        Deserialize a JSON string into an ECSConfig object.

        :param json_data: JSON string to deserialize.
        """
        if not json_data:
            return
        self.cluster_arn = json_data.get("cluster_arn", None)
        self.cluster_name = json_data.get("cluster_name", None)
