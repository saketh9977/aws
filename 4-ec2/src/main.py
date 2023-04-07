from datetime import datetime, timezone
import pprint
import time

import boto3

aws_region = 'us-east-1'

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
            raise Exception(f'instance id = {instance_id} is missing in response')
        
        status = response['Reservations'][0]['Instances'][0]['State']['Name']
        print___(f'instance id = {instance_id}, status = {status}')

        if status in undesired_state_list:
            raise Exception(f'instance id = {instance_id}, status = {status}')

        if status in desired_state_list:
            print___(f'not polling as instance status = {status}')
            return status

        print___(f'sleeping for {poll_freq_in_sec}s...')
        time.sleep(poll_freq_in_sec)
        print___('awake')

def wait_for_ssm_agent(ssm_client, instance_id, desired_state_list, undesired_state_list, poll_freq_in_sec):
    
    """
        If PingStatus = Online then SSM agent is online on that EC2
        SSM agent listens for incoming commands and executes them.
    """

    while True:

        print___(f"fetching SSM agent status on instance id = {instance_id}...")

        response = ssm_client.describe_instance_information(
            InstanceInformationFilterList=[
                {
                    'key': 'InstanceIds',
                    'valueSet': [instance_id]
                }
            ]
        )

        if len(response['InstanceInformationList']) <= 0:
            continue

        if response['InstanceInformationList'][0]['InstanceId'] != instance_id:
            continue

        ssm_agent_status = response['InstanceInformationList'][0]['PingStatus']
        print___(f"ssm agent = {ssm_agent_status}")

        if ssm_agent_status in desired_state_list:
            print___(f"Not polling as SSM Agent is {ssm_agent_status}")
            return
        
        if ssm_agent_status in undesired_state_list:
            raise Exception(f"SSM agent {ssm_agent_status}")
        
def execute_commands_on_ec2(ssm_client, command_list, instance_id):

    """
        references
            1. CLI examples - https://docs.aws.amazon.com/cli/latest/reference/ssm/send-command.html
            2. Boto3 send_command API syntax - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/send_command.html
            3. execution timeout - https://github.com/boto/boto3/issues/1343#issuecomment-345778729
    """

    print___(f'running the following commands on ec2 instance id = {instance_id} -')
    pprint.pprint(command_list)

    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        TimeoutSeconds=180,
        Parameters={
            'commands': command_list,
            'executionTimeout': ['5400']
        },
        OutputS3BucketName='test-4323',
        OutputS3KeyPrefix='ssm-logs'
    )
    command_id = response['Command']['CommandId']
    print___(f'triggered, command id = {command_id}')

    return command_id

def poll_ec2_commands(ssm_client, command_id, instance_id, poll_freq_in_sec):

    undesired_state_list = ['Cancelled', 'TimedOut', 'Failed']
    desired_state_list = ['Success']

    while True:
        print___(f'fetching command status command id = {command_id}...')

        response = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )

        status = response['Status']
        print___(f"command id = {command_id} execution status = {status}")

        if status in undesired_state_list:
            print___(f"STDOUT content = ")
            print___(response['StandardOutputContent'])

            print___(f"STDERR content = ")
            print___(response['StandardErrorContent'])

            print___(f"STDOUT = {response['StandardOutputUrl']}")
            print___(f"STDERR = {response['StandardErrorUrl']}")
            raise Exception(f"command id = {command_id} whose exec. status = {status} on ec2 instance id = {instance_id}")
        
        if status in desired_state_list:
            print___(f'not polling as command exec. status = {status}')

            print___(f"STDOUT content = ")
            print___(response['StandardOutputContent'])

            print___(f"STDERR content = ")
            print___(response['StandardErrorContent'])

            print___(f"STDOUT = {response['StandardOutputUrl']}")
            print___(f"STDERR = {response['StandardErrorUrl']}")
            return

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
    ec2_client = boto3.client('ec2', region_name=aws_region) 

    instance_id = launch_ec2(ec2_client)
    desired_state_list = ['running']
    undesired_state_list = ['terminated', 'stopped']
    poll_ec2_status(ec2_client, instance_id, desired_state_list, undesired_state_list, 20)
    
    ssm_client = boto3.client('ssm', aws_region)
    desired_state_list = ['Online']
    undesired_state_list = ['ConnectionLost', 'Inactive']
    wait_for_ssm_agent(ssm_client, instance_id, desired_state_list, undesired_state_list, 5)

    command_list = [
        'date',
        'pwd',
        'aws s3 ls s3://test-4323/',
        'date'
    ]
    command_id = execute_commands_on_ec2(ssm_client, command_list, instance_id)
    poll_ec2_commands(ssm_client, command_id, instance_id, 10)

    terminate_ec2(ec2_client, instance_id)
    desired_state_list = ['terminated']
    undesired_state_list = ['stopped']
    poll_ec2_status(ec2_client, instance_id, desired_state_list, undesired_state_list, 20)

    print___('main: ending...')

if __name__ == '__main__':
    main()