import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the environments
environments = os.getenv("environments", "dev,qa,prod").split(',')

def stop_ec2_instances():
    ec2 = boto3.resource('ec2')
    
    for env in environments:
        # Find instances with the matching environment tag
        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:Environment', 'Values': [env]},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        
        for instance in instances:
            try:
                instance.stop()
                print(f"Stopping {env.upper()} EC2 instance with ID: {instance.id}")
            except Exception as e:
                print(f"Error stopping {env.upper()} EC2 instance {instance.id}: {str(e)}")

if __name__ == "__main__":
    stop_ec2_instances()