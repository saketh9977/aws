from datetime import datetime, timezone
import pprint
import time

import boto3

def print___(msg):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    print(f"{timestamp}: {msg}")

def launch_ec2(ec2_client):

    print___('launching EC2...')

    response = ec2_client.run_instances(
        ImageId='ami-00c39f71452c08778', # Amazon Linux 2023 AMI,
        InstanceType='t2.micro',
        KeyName='ssh-key',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=['sg-0972fd810284bf2cd'],
        IamInstanceProfile={
            'Name': 'explore-iam'
        },
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Resource',
                    'Value': 'EC2'
                },
                {
                    'Key': 'Resource Name',
                    'Value': 'explore-ec2'
                }
            ]
        }]
    )

    # pprint.pprint(response)
    return response['Instances'][0]['InstanceId']

def poll_ec2_launch(ec2_client, instance_id):

    poll_delay = 10 # seconds

    while True:

        print___(f'describing instance with instance id = {instance_id}...')
        response = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )
        # pprint.pprint(response)

        if response['Reservations'][0]['Instances'][0]['InstanceId'] != instance_id:
            raise(f'instance id = {instance_id} is missing in response')
        
        status = response['Reservations'][0]['Instances'][0]['State']['Name']
        print___(f'status = {status}')

        if status in ['terminated', 'stopped']:
            raise(f'instance {status}')

        if status == 'running':
            return status

        print___(f'sleeping for {poll_delay}s...')
        time.sleep(poll_delay)
        print___('awake')

def main():
    print___('main: starting...')

    ec2_client = boto3.client('ec2', region_name='us-east-1') 
    instance_id = launch_ec2(ec2_client)
    poll_ec2_launch(ec2_client, instance_id)
    print___('main: ending...')

if __name__ == '__main__':
    main()