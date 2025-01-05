import ipaddress
from click import echo
from meta import DRY_RUN
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
from utils.logging import log, log_warning
from services.config.env_config import EnvironmentConfig


class VPC:

    def __init__(self, env_config: EnvironmentConfig):
        self.name = env_config.config.name
        self.region = env_config.config.region
        self.env_config = env_config
        self.config = env_config.config.vpc
        self.client = boto3.client('ec2', region_name=self.region)

    def _create(self):
        vpc_response = {"Vpc": None}
        try:
            vpc_response = self.client.create_vpc(
                CidrBlock=self.config.cidr,
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': self.config.vpc_name
                            },
                            {
                                'Key': 'Publisher',
                                'Value': "kobidh"
                            }
                        ]
                    },
                ],
                DryRun=DRY_RUN,
                InstanceTenancy='default'
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                log_warning(
                    "DryRun passed: You have the required permissions to create the VPC.")
                vpc_response = {
                    "Vpc": {"VpcId": f"dummy-vpc-{"".join(str(uuid4()).split("-")[:3])}"}}
        self.config.vpc_id = vpc_response.get('Vpc')['VpcId']
        log(f"VPC created with id: {self.config.vpc_id}")
        subnets_response = []
        for subnet in self.config.subnets["private"]:
            subnet_response = {"Subnet": None}
            try:
                subnet_response = self.client.create_subnet(
                    CidrBlock=str(subnet["cidr"]),
                    VpcId=self.config.vpc_id,
                    AvailabilityZone=subnet["az"],
                    TagSpecifications=[
                        {
                            'ResourceType': 'subnet',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': subnet["name"]
                                },
                                {
                                    'Key': 'Publisher',
                                    'Value': "kobidh"
                                }
                            ]
                        },
                    ],
                    DryRun=DRY_RUN
                )
            except ClientError as e:
                if e.response['Error']['Code'] == 'DryRunOperation':
                    log_warning(
                        "DryRun passed: You have the required permissions to create the subnet.")
                    subnet_response = {"Subnet": {
                        "SubnetId": f"dummy-subnet-{"".join(str(uuid4()).split("-")[:3])}"}}
            log(f"Subnet created with id: {subnet_response.get('Subnet').get("SubnetId")}")
            subnets_response.append(subnet_response.get('Subnet'))
        return {
            "Vpc": vpc_response.get('Vpc'),
            "Subnets": subnets_response
        }

    def _get(self):
        vpcs_response = None
        try:
            vpcs_response = self.client.describe_vpcs(
                Filters=[
                    {
                        'Name': 'cidr',
                        'Values': [
                            self.config.cidr,
                        ]
                    },
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            self.config.vpc_name,
                        ]
                    },
                    {
                        'Name': 'tag:Publisher',
                        'Values': [
                            "kobidh",
                        ]
                    }
                ],
                DryRun=DRY_RUN
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                log_warning(
                    "DryRun passed: You have the required permissions to describe the VPCs.")
                vpcs_response = {
                    "Vpcs": [{"VpcId": f"dummy-vpc-{"".join(str(uuid4()).split("-")[:3])}"}]}
        if len(vpcs_response.get('Vpcs')) == 0:
            return {'Vpc': None}
        vpc_response = vpcs_response.get('Vpcs')[0]
        self.config.vpc_id = vpc_response['VpcId']
        log(f"VPC found with id: {self.config.vpc_id}")
        filters = [
            {
                'Name': 'vpc-id',
                'Values': [self.config.vpc_id]
            }
        ]
        subnets_response = None
        try:
            subnets_response = self.client.describe_subnets(
                Filters=filters,
                DryRun=DRY_RUN
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                log_warning(
                    "DryRun passed: You have the required permissions to describe the Subnets.")
                subnets_response = {"Subnets": [
                    {"SubnetId": f"dummy-subnet-{"".join(str(uuid4()).split("-")[:3])}"}]}
        subnets_response['Vpc'] = vpc_response
        log(f"Subnets found with ids: {[resp.get("SubnetId") for resp in subnets_response.get("Subnets")]}")
        return subnets_response

    def _get_or_create(self):
        response = self._get()
        if not response['Vpc']:
            return self._create()
        self.config.vpc_id = response['Vpc']['VpcId']
        return response

    def _delete(self):
        response = self._get()
        if not response['Vpc']:
            return
        self.config.vpc_id = response['Vpc']['VpcId']
        for subnet in response['Subnets']:
            try:
                response = self.client.delete_subnet(
                    SubnetId=subnet['SubnetId'],
                    DryRun=DRY_RUN
                )
            except ClientError as e:
                if e.response['Error']['Code'] == 'DryRunOperation':
                    log_warning(
                        "DryRun passed: You have the required permissions to delete the Subnet.")
        try:
            response = self.client.delete_vpc(
                VpcId=self.config.vpc_id,
                DryRun=DRY_RUN
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                log_warning(
                    "DryRun passed: You have the required permissions to delete the VPC.")
        self.config.vpc_id = None

    def describe(self):
        self._get_or_create()

    def _update(self):
        pass

    def run(self):
        if self.env_config.get():
            self._get_or_create()
        else:
            self._delete()
