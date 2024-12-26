import json
import boto3
from typing import Annotated
from fastapi import APIRouter, Form
from ..utilities.env_handler import get_env_vars
from ..utilities.app_describe import AppDescribe

router = APIRouter()

@router.get("/", tags=["apps"])
async def read_apps():
    apigateway_client = boto3.client("apigatewayv2")
    response = apigateway_client.get_apis()
    return response

@router.post("/create", tags=["apps"])
async def create_app(
    name: Annotated[str, Form()],
    # region: Annotated[str, Form()],
):
    apigateway_response = None
    ecr_response = None

    # apigateway_client = boto3.client("apigatewayv2")
    # apigateway_response = apigateway_client.create_api(
    #     Name=name,
    #     ProtocolType='HTTP',
    #     Tags={
    #         'publisher': 'kobidh'
    #     },
    # )
    # ecr_client = boto3.client("ecr")
    # ecr_response = ecr_client.create_repository(
    #     repositoryName=name,
    #     tags=[
    #         {
    #             'Key': 'publisher',
    #             'Value': 'kobidh'
    #         },
    #     ],
    #     imageTagMutability='MUTABLE',
    #     imageScanningConfiguration={
    #         'scanOnPush': False
    #     },
    #     encryptionConfiguration={
    #         'encryptionType': 'AES256',
    #     }
    # )

    s3_client = boto3.client("s3")
    describe = AppDescribe(
        name=name,
        api_gateway=apigateway_response,
        ecr_response=ecr_response,
    )
    s3_client.put_object(
        Bucket=get_env_vars("s3_app_describe_name"),
        Key=f"{name}.json",
        Body=json.dumps(describe.__dict__, indent=2)
    )
    return {
        "message": "App created successfully",
        "API_GATEWAY": apigateway_response,
        "ECR": ecr_response
    }
