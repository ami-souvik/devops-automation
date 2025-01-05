import ipaddress
from click import echo
from meta import DRY_RUN
from utils.logging import log
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
        self.client = boto3.client('ecs', region_name=self.region)

    def _create(self):
        echo("Creating ECS Resources...")
        if DRY_RUN:
            # Check for permissions also
            cluster_arn = f"arn:aws:ecs:{self.region}:{self.env_config.get_account_id()}:cluster/{self.config.cluster_name}"
            log(f"Cluster created with arn: {cluster_arn}")
            return {'cluster': {'clusterArn': cluster_arn }}
        else:
            cluster_response = self.client.create_cluster(
                clusterName=self.config.cluster_name,
                tags=[{'key': tag['Key'], 'value': tag['Value']} for tag in self.config.get_tags()]
            )
            log(f"Cluster created with arn: {cluster_response["cluster"]["clusterArn"]}")
            return cluster_response

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
            return {'cluster': None}
        cluster = clusters_response.get('clusters')[0]
        if cluster.get('status') == 'INACTIVE':
            return {'cluster': None}
        log(f"Cluster found with arn: {cluster["clusterArn"]}")
        return {'cluster': cluster}

    def _get_or_create(self):
        response = self._get()
        if not response.get('cluster'):
            response = self._create()
        self.config.cluster_arn = response['cluster']['clusterArn']
        return response

    def _delete(self):
        response = self._get()
        if not response['cluster']:
            return
        echo("Deleting ECS Resources...")
        self.config.cluster_arn = response['cluster']['clusterArn']
        if DRY_RUN:
            # Check for permissions also
            cluster_arn = f"arn:aws:ecs:{self.region}:{self.env_config.get_account_id()}:cluster/{self.config.cluster_name}"
            log(f"Cluster deleted with arn: {cluster_arn}")
            return {'cluster': {'clusterArn': cluster_arn }}
        else:
            self.client.delete_cluster(
                cluster=self.config.cluster_arn
            )
        self.config.cluster_arn = None

    def _update(self):
        pass

    def run(self):
        record = self.env_config.get()
        if record and record.get('configuration') and record.get('configuration').get('ecs'):
            self._get_or_create()
        else:
            self._delete()
