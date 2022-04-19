import boto3
import json
import sys

class Ec2Describer:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client("ec2")

    def describe_instance_type_offerings(self):
        response = self.client.describe_instance_type_offerings(
            LocationType="availability-zone",
            # LocationType="availability-zone-id",
            Filters=[
                {
                    "Name": "instance-type",
                    "Values": ["g5.xlarge"]
                }
            ]
        )
        return response["InstanceTypeOfferings"]
