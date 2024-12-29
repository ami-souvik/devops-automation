from .aws_resource import AWSResource

class APIGateway(AWSResource):
    def __init__(self, region: str = None):
        super().__init__("apigatewayv2", region)

    def get(self, resource_arn: str):
        arn_parts = resource_arn.split(":")
        resource_path = arn_parts[5]
        resource_parts = resource_path.split("/")
        api_id = resource_parts[2]
        # Get resource details
        try:
            return self.client.get_api(ApiId=api_id)
        except self.client.exceptions.NotFoundException:
            return f"API Resource with ID {api_id} not found"
        except Exception as e:
            return f"An error occurred: {e}"

    def create(self, name):
        return self.client.create_api(
            Name=name,
            ProtocolType='HTTP',
            Tags=self.get_v2_tags(name),
        )
    
    def delete(self, resource_arn: str):
        arn_parts = resource_arn.split(":")
        resource_path = arn_parts[5]
        resource_parts = resource_path.split("/")
        api_id = resource_parts[2]
        try:
            return self.client.delete_api(ApiId=api_id)
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}"
