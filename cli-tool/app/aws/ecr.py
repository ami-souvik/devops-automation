from .resource import AWSResource
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
 
class ECR(AWSResource):
    def __init__(self, region: str = None):
        super().__init__("ecr", region)

    def check_and_create(self, repo_names):
        """
        Checks if ECR repositories exist and creates them if they don't.

        :param repo_names: List of repository names to check and create.
        """
        try:
            # Fetch existing repositories using describe_repositories API
            existing_repos = set()
            response = self.client.describe_repositories()

            # Collect existing repositories into a set
            existing_repos.update(repo['repositoryName'] for repo in response['repositories'])

            for repo_name in repo_names:
                if repo_name in existing_repos:
                    print(f"ECR Repository '{repo_name}' already exists.")
                else:
                    print(f"ECR Repository '{repo_name}' does not exist. Creating...")
                    response = self.client.create_repository(repositoryName=repo_name)
                    repo_uri = response['repository']['repositoryUri']
                    print(f"ECR Repository '{repo_name}' created successfully: {repo_uri}")

        except self.client.exceptions.RepositoryNotFoundException:
            print("Repository not found.")
        except NoCredentialsError:
            print("AWS credentials not found. Please configure your credentials.")
        except PartialCredentialsError:
            print("Incomplete AWS credentials configuration.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get(self, names: list[str]):
        response = self.client.describe_repositories(
            registryId=self.account_id,
            repositoryNames=names
        )
        return response['repositories']

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
            return f"An error occurred: {e}"