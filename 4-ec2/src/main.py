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

def poll_ec2_status(ec2_client, instance_id, desired_state_list, undesired_state_list, poll_freq_in_sec):

    while True:

        print___(f'describing instance with instance id = {instance_id}...')
        response = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )
        # pprint.pprint(response)

        if response['Reservations'][0]['Instances'][0]['InstanceId'] != instance_id:
            raise(f'instance id = {instance_id} is missing in response')
        
        status = response['Reservations'][0]['Instances'][0]['State']['Name']
        print___(f'instance id = {instance_id}, status = {status}')

        if status in undesired_state_list:
            raise(f'instance id = {instance_id}, status = {status}')

        if status in desired_state_list:
            return status

        print___(f'sleeping for {poll_freq_in_sec}s...')
        time.sleep(poll_freq_in_sec)
        print___('awake')

def terminate_ec2(ec2_client, instance_id):
    print___(f"terminating ec2 with instance id = {instance_id}...")

    response = ec2_client.terminate_instances(
        InstanceIds=[instance_id]
    )

    # pprint.pprint(response)
    print___(f'triggered termination of ec2 with instance id = {instance_id}')

def main():
    print___('main: starting...')

    ec2_client = boto3.client('ec2', region_name='us-east-1') 
    instance_id = launch_ec2(ec2_client)

    desired_state_list = ['running']
    undesired_state_list = ['terminated', 'stopped']
    poll_ec2_status(ec2_client, instance_id, desired_state_list, undesired_state_list, 10)

    

    terminate_ec2(ec2_client, instance_id)

    desired_state_list = ['terminated']
    undesired_state_list = ['running', 'stopped']
    poll_ec2_status(ec2_client, instance_id, desired_state_list, undesired_state_list, 10)


    print___('main: ending...')

if __name__ == '__main__':
    main()