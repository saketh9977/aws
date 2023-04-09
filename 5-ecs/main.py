import boto3

from datetime import datetime, timezone
import pprint

aws_region = 'us-east-1'
s3_bucket = 'test-4323'

def upload_str_to_s3_as_obj(s3_client, content: str):

    response = s3_client.put_object(
        Body=content,
        Bucket=s3_bucket,
        Key='ecs-out.txt'
    )

    pprint.pprint(response)


def main():
    print('main: started')
    
    s3_client = boto3.client('s3', region_name=aws_region)

    content = datetime.now().replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z')
    upload_str_to_s3_as_obj(s3_client, content)

    print('main: ended')


if __name__ == '__main__':
    main()
