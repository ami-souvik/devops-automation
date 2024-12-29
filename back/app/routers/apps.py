import boto3
from collections import defaultdict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from botocore.exceptions import BotoCoreError, ClientError
from ..services.api_gateway import APIGateway
from ..services.ecr import ECR

router = APIRouter()

@router.get("/list", tags=["list_apps"])
async def read_apps(az: str):
    """
    Endpoint to list and group AWS resources by the "name" tag
    for resources with the "publisher" tag equal to "kobidh".

    Returns:
        A dictionary grouping resource ARNs by their "name" tag.
    """
    try:
        client = boto3.client('resourcegroupstaggingapi', region_name=az)
        response = client.get_resources(
            TagFilters=[{'Key': 'publisher', 'Values': ['kobidh']}]
        )
        grouped_resources = defaultdict(dict)
        # Group resources by their Resource ARN
        for resource in response["ResourceTagMappingList"]:
            tags = {tag["Key"]: tag["Value"] for tag in resource["Tags"]}
            resource_arn = resource["ResourceARN"]
            resource_key = resource_arn.split(":")[2]

            name_tag = tags.get("name", "Unknown")
            grouped_resources[name_tag][resource_key] = {
                "resource_arn": resource["ResourceARN"]
            }
        apps = []
        for name_tag in grouped_resources:
            apps.append({
                "name": name_tag,
                **grouped_resources[name_tag]
            })
        return {
            "availability_zone": az,
            "apps": apps
        }
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{app_id}", tags=["get_app"])
async def get_app(
    app_id: str,
    az: str
):
    try:
        client = boto3.client('resourcegroupstaggingapi', region_name=az)
        response = client.get_resources(
            TagFilters=[{'Key': 'publisher', 'Values': ['kobidh']}, {'Key': 'name', 'Values': [app_id]}]
        )
        grouped_resources = defaultdict(dict)
        grouped_resources["availability_zone"] = az

        # Group resources by their Resource ARN
        for resource in response["ResourceTagMappingList"]:
            resource_arn = resource["ResourceARN"]
            resource_key = resource_arn.split(":")[2]
            if resource_key == "apigateway":
                grouped_resources[resource_key] = APIGateway(az).get(resource_arn)
            elif resource_key == "ecr":
                grouped_resources[resource_key] = ECR(az).get(resource_arn)
        return grouped_resources
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))


class CreateApp(BaseModel):
    app_name: str
    availability_zone: str

@router.post("/create", tags=["create_app"])
async def create_app(
    item: CreateApp,
):
    apigateway_response = None
    ecr_response = None

    apigateway_response = APIGateway(item.availability_zone).create(item.app_name)
    ecr_response = ECR(item.availability_zone).create(item.app_name)
    return {
        "message": "App created successfully",
        "app_name": item.app_name,
        "availability_zone": item.availability_zone,
        "API_GATEWAY": apigateway_response,
        "ECR": ecr_response
    }

@router.delete("/delete/{app_id}", tags=["delete_app"])
async def delete_app(
    app_id: str,
    az: str
):
    try:
        client = boto3.client('resourcegroupstaggingapi', region_name=az)
        response = client.get_resources(
            TagFilters=[{'Key': 'publisher', 'Values': ['kobidh']}, {'Key': 'name', 'Values': [app_id]}]
        )
        grouped_resources = defaultdict(dict)
        grouped_resources["availability_zone"] = az

        # Group resources by their Resource ARN
        for resource in response["ResourceTagMappingList"]:
            resource_arn = resource["ResourceARN"]
            resource_key = resource_arn.split(":")[2]
            if resource_key == "apigateway":
                grouped_resources[resource_key] = APIGateway(az).delete(resource_arn)
            elif resource_key == "ecr":
                grouped_resources[resource_key] = ECR(az).delete(resource_arn)
        return grouped_resources
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))
