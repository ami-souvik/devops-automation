import ipaddress
from click import echo
from meta import DRY_RUN
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from utils.logging import log, log_warning
from services.config.env_config import EnvironmentConfig


class ECS:

    def __init__(self, env_config: EnvironmentConfig):
        self.name = env_config.config.name
        self.region = env_config.config.region
        self.env_config = env_config
        self.config = env_config.config.ecs
        self.client = boto3.client('ec2', region_name=self.region)
        self.iam_client = boto3.client("iam")

    def _create(self):
        pass

    def _get(self):
        clusters_response = None
        try:
            clusters_response = self.client.describe_clusters(
                clusters=[
                    self.config.cluster_name
                ]
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                log_warning(
                    "DryRun passed: You have the required permissions to describe the VPCs.")
                clusters_response = {
                    "clusters": [{"clusterName": self.config.cluster_name}]
                }
        if len(clusters_response.get('clusters')) == 0:
            return {'Cluster': None}
        return {'Cluster': clusters_response.get('clusters')[0]}

    def _get_or_create(self):
        response = self._get()
        pass

    def _delete(self):
        pass

    def _update(self):
        pass

    def run(self):
        if self.env_config.get():
            self._get_or_create()
        else:
            self._delete()
