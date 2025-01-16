import boto3
import os
from dotenv import load_dotenv

load_dotenv()

environments = os.getenv("environments", "dev,qa,prod").split(',')

def deploy_ec2_instances():
    ec2 = boto3.resource('ec2')
    
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
            print(f"Launched {env.upper()} EC2 instance with ID: {instance.id}")
        except Exception as e:
            print(f"Error launching {env.upper()} EC2 instance: {str(e)}")
    
    return instances

if __name__ == "__main__":
    deploy_ec2_instances()