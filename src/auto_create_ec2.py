import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the environments
environments = os.getenv("environments", "dev,qa,prod").split(',')

def deploy_ec2_instances():
    ec2 = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')
    
    # Get available availability zones
    response = ec2_client.describe_availability_zones()
    available_zones = [zone['ZoneName'] for zone in response['AvailabilityZones']]
    
    # Assign zones to environments
    zone_mapping = {
        'dev': available_zones[0],
        'qa': available_zones[1],
        'prod': available_zones[2]
    }
    
    instances = []
    for env in environments:
        try:
            security_group = os.getenv(f"SecurityGroup{env.capitalize()}")
            if not security_group:
                raise ValueError(f"Security group for {env} environment not set")

            instance = ec2.create_instances(
                ImageId=os.getenv("ImageId"),
                MinCount=1,
                MaxCount=1,
                InstanceType='t2.micro',
                KeyName=os.getenv("KeyName"),
                SecurityGroupIds=[security_group],
                Placement={
                    'AvailabilityZone': zone_mapping[env]
                },
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {'Key': 'Name', 'Value': f'EC2-{env.upper()}'},
                            {'Key': 'Environment', 'Value': env}
                        ]
                    },
                ]
            )[0]
            instances.append(instance)
            print(f"Launched {env.upper()} EC2 instance with ID: {instance.id} in zone: {zone_mapping[env]}")
        except Exception as e:
            print(f"Error launching {env.upper()} EC2 instance: {str(e)}")
    
    return instances

if __name__ == "__main__":
    deploy_ec2_instances()
