from .aws_resource import AWSResource
 
class ECS(AWSResource):
    def __init__(self, region: str = None):
        super().__init__("ecs", region)

    def create_capacity_provider(self, name):
        return self.client.create_capacity_provider(
            name='string',
            autoScalingGroupProvider={
                'autoScalingGroupArn': 'string',
                'managedScaling': {
                    'status': 'ENABLED'|'DISABLED',
                    'targetCapacity': 123,
                    'minimumScalingStepSize': 123,
                    'maximumScalingStepSize': 123,
                    'instanceWarmupPeriod': 123
                },
                'managedTerminationProtection': 'ENABLED'|'DISABLED',
                'managedDraining': 'ENABLED'|'DISABLED'
            },
            tags=[
                {
                    'key': 'string',
                    'value': 'string'
                },
            ]
        )

    def create_cluster(self, name):
        return self.client.create_cluster(
            clusterName=name,
            tags=self.get_tags(name),
            settings=[
                {
                    'name': 'containerInsights',
                    'value': 'disabled'
                },
            ],
            configuration={
                'executeCommandConfiguration': {
                    'kmsKeyId': 'string',
                    'logging': 'NONE'|'DEFAULT'|'OVERRIDE',
                    'logConfiguration': {
                        'cloudWatchLogGroupName': 'string',
                        'cloudWatchEncryptionEnabled': True|False,
                        's3BucketName': 'string',
                        's3EncryptionEnabled': True|False,
                        's3KeyPrefix': 'string'
                    }
                },
                'managedStorageConfiguration': {
                    'kmsKeyId': 'string',
                    'fargateEphemeralStorageKmsKeyId': 'string'
                }
            },
            capacityProviders=[
                'string',
            ],
            defaultCapacityProviderStrategy=[
                {
                    'capacityProvider': 'string',
                    'weight': 123,
                    'base': 123
                },
            ],
            serviceConnectDefaults={
                'namespace': 'string'
            }
        )

    def create_task_definition(self, name):
        return self.client.create_task_set(
            service='string',
            cluster='string',
            externalId='string',
            taskDefinition='string',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        'string',
                    ],
                    'securityGroups': [
                        'string',
                    ],
                    'assignPublicIp': 'ENABLED'|'DISABLED'
                }
            },
            loadBalancers=[
                {
                    'targetGroupArn': 'string',
                    'loadBalancerName': 'string',
                    'containerName': 'string',
                    'containerPort': 123
                },
            ],
            serviceRegistries=[
                {
                    'registryArn': 'string',
                    'port': 123,
                    'containerName': 'string',
                    'containerPort': 123
                },
            ],
            launchType='EC2'|'FARGATE'|'EXTERNAL',
            capacityProviderStrategy=[
                {
                    'capacityProvider': 'string',
                    'weight': 123,
                    'base': 123
                },
            ],
            platformVersion='string',
            scale={
                'value': 123.0,
                'unit': 'PERCENT'
            },
            clientToken='string',
            tags=self.get_tags(name),
        )

    def create(self, name):
        capacity_provider_response = self.create_capacity_provider(name)
        cluster_response = self.create_cluster(name)
        task_definition_response = self.create_task_definition(name)
        pass
    
    def get(self, resource_arn: str):
        arn_parts = resource_arn.split(":")
        resource_part = arn_parts[-1]
        repository_name = resource_part.split("/")[-1]
        response = self.client.describe_repositories(
            registryId=arn_parts[4],
            repositoryNames=[repository_name]
        )
        return response['repositories'][0]

    def delete(self, resource_arn: str):
        arn_parts = resource_arn.split(":")
        resource_part = arn_parts[-1]
        repository_name = resource_part.split("/")[-1]
        try:
            return self.client.delete_repository(
                repositoryName=repository_name,
                force=True|False
            )
        except Exception as e:
            return f"An error occurred: {e}"