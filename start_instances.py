import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the environments
environments = os.getenv("environments", "dev,qa,prod").split(',')

def start_ec2_instances():
    ec2 = boto3.resource('ec2')
    
    for env in environments:
        # Find stopped instances with the matching environment tag
        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:Environment', 'Values': [env]},
                {'Name': 'instance-state-name', 'Values': ['stopped']}
            ]
        )
        
        for instance in instances:
            try:
                instance.start()
                instance.wait_until_running()
                print(f"Started {env.upper()} EC2 instance with ID: {instance.id}")
                
                # Refresh instance information
                instance.reload()
                print(f"New public IP: {instance.public_ip_address}")
                print(f"New private IP: {instance.private_ip_address}")
            except Exception as e:
                print(f"Error starting {env.upper()} EC2 instance {instance.id}: {str(e)}")

if __name__ == "__main__":
    start_ec2_instances()
