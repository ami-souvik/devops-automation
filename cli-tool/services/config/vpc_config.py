import ipaddress
import boto3
from click import echo
from services.config import Config

class VPCConfig(Config):
    """
        Contains VPC configuration details
    """
    def __init__(self, name: str, region: str):
        self.name = name
        self.region = region
        self.vpc_id = None
        self.vpc_name = f"{name}-vpc"
        cidr = ipaddress.IPv4Network("10.10.0.0/16")
        self.cidr = str(cidr)
        subnets_list = list(cidr.subnets(new_prefix=22))

        session = boto3.session.Session()
        self.session = session.resource('ec2')
        self.client = boto3.client('ec2', region_name=self.region)
        index = 0
        azones = self._get_azs()
        private_subnets = []
        for az in azones:
            private_subnets.append({
                "name": f"{self.name}-subnet-{az}",
                "az": az,
                "cidr": str(subnets_list[index]),
            })
            index += 2
        self.subnets = {
            "private": private_subnets
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VPCConfig):
            return (self.vpc_id == other.vpc_id and self.vpc_name == other.vpc_name and self.cidr == other.cidr
                    and self.subnets == other.subnets)
        return False
    
    def _get_azs(self):
        """
        Fetches the available availability zones for a given AWS region.

        :param region: AWS region name (e.g., 'ap-south-1').
        :return: List of availability zone names.
        """
        try:
            response = self.client.describe_availability_zones(
                Filters=[
                    {'Name': 'region-name', 'Values': [self.region]},
                    {'Name': 'state', 'Values': ['available']}  # Only zones that are available
                ]
            )
            zones = [az['ZoneName'] for az in response['AvailabilityZones']]
            return zones
        except Exception as e:
            echo(f"Error fetching availability zones: {str(e)}")
            return []

    def json(self):
        return {
            "vpc_id": self.vpc_id,
            "vpc_name": self.vpc_name,
            "cidr": self.cidr,
            "subnets": self.subnets
        }
    
    def parse_json(self, json_data: dict):
        """
        Deserialize a JSON string into an VPCConfig object.

        :param json_data: JSON string to deserialize.
        """
        if not json_data:
            return
        self.vpc_id = json_data.get("vpc_id", None)
        self.vpc_name = json_data.get("vpc_name", None)
        self.cidr = json_data.get("cidr", None)
        self.subnets = json_data.get("subnets", None)
