import boto3


from src.constants import *
from src.utils import (
    print_
)

def create_table(dynamodb):

    table = None

    try:
        table = dynamodb.create_table(
            TableName=TABLE,
            KeySchema=[
                {
                    "AttributeName": "pin_code",
                    "KeyType": "HASH" # Partition Key
                },
                {
                    "AttributeName": "area_name",
                    "KeyType": "RANGE" # Sort Key
                },

            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "pin_code",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "area_name",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            }
        )

        table.wait_until_exists()
        print_(f"dynamo-db: {TABLE} table created")

    except Exception as e:
        print_(f"dynamo-db: {str(e)}")
        print_(f"dynamo-db: seems like {TABLE} table aleady exists in dynamoDB")
        table = dynamodb.Table(TABLE)
        table.wait_until_exists()

    return table

def insert_into_dynamodb(data):

    print_('dynamo-db: storing...')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = create_table(dynamodb)

    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

    print_('dynamo-db: stored')
