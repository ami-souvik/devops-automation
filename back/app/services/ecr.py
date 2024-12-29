from .aws_resource import AWSResource
 
class ECR(AWSResource):
    def __init__(self, region: str = None):
        super().__init__("ecr", region)

    def get(self, resource_arn: str):
        arn_parts = resource_arn.split(":")
        resource_part = arn_parts[-1]
        repository_name = resource_part.split("/")[-1]
        response = self.client.describe_repositories(
            registryId=arn_parts[4],
            repositoryNames=[repository_name]
        )
        return response['repositories'][0]

    def create(self, name):
        return self.client.create_repository(
            repositoryName=name,
            tags=self.get_tags(name),
            imageTagMutability='MUTABLE',
            imageScanningConfiguration={
                'scanOnPush': False
            },
            encryptionConfiguration={
                'encryptionType': 'AES256',
            }
        )
    
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
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"