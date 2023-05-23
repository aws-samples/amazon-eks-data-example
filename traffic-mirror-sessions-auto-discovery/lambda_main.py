# ec2 create event trigger this lambda function
import json
import boto3
import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()

# create mirror target
def create_mirror_target(ec2_client, target_arn):
    try:
        response = ec2_client.create_mirror_target(
            SourceRegion='us-east-1',
            SourceResource=target_arn
        )
        return response
    except ClientError as e:
        logger.error(e)
        return e

def lambda_handler(event, context):
    logger.info(event)
    # Get the service resource
    ec2 = boto3.resource('ec2')
    # Get the instance ID
    instance_id = event['detail']['instance-id']
    # Get the instance
    instance = ec2.Instance(instance_id)
    # Get the instance state
    state = instance.state['Name']
    # Get the instance type
    instance_type = instance.instance_type
    # Get the instance region
    region = os.environ['AWS_REGION']
    # Get the instance availability zone
    zone = instance.placement['AvailabilityZone']
    # Get the instance public IP
    public_ip = instance.public_ip_address
    # Get the instance private IP
    private_ip = instance.private_ip_address
    # Get the instance launch time
    launch_time = instance.launch_time
    # Get the instance tags
    tags = instance.tags
    # Get the instance AMI
    ami = instance.image.id
    # Get the instance key name
    key_name = instance.key_name
    # Get the instance platform
    platform = instance.platform
    platform = instance.platform
    # Get the instance architecture
    architecture = instance.architecture
    # Get the instance architecture
    architecture = instance.architecture
    # Get the instance root device type
    root_device_type = instance.root_device_type
    # Get the instance root device name
    root_device_name = instance.root_device_name
    # Get the instance virtualization type
    virtualization_type = instance.virtualization_type
    # Get the instance monitoring state
    monitoring_state = instance.monitoring['State']
    # Get the instance Enis
    enis = instance.network_interfaces
    # Get all eni ids
    eni_ids = [eni['NetworkInterfaceId'] for eni in enis]
    # Get the instance security groups
    security_groups = instance.security_groups
