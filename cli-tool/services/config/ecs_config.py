class ECSConfig:
    """
        Contains ECS configuration details
    """
    class Template:
        def __init__(self, name: str, region: str):
            self.name = name
            self.region = region
            self.min_instances = 1
            self.max_instances = 3
            self.spot_min_instances = 1
            self.spot_min_instances = 3
            self.instance_type = "t2.micro"
            self.ssh_key_name = f"{name}-cluster-key"
            self.ami_id = ""
