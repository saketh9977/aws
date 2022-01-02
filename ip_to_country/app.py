import requests
import boto3

IP_ADDRESS = 'ip_address'


def create_table(dynamodb):

    table = None

    try:
        table = dynamodb.create_table(
            TableName=IP_ADDRESS,
            KeySchema=[
                {
                    "AttributeName": "ip_address",
                    "KeyType": "HASH" # Partition key
                },
                {
                    "AttributeName": "country",
                    "KeyType": "RANGE" # Sort Key
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "ip_address",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "country",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            }
        )

        table.wait_until_exists()
        print("ip table created")

    except Exception as e:
        print(f"seems like ip table aleady exists in dynamoDB")
        table = dynamodb.Table(IP_ADDRESS)
        table.wait_until_exists()

    return table

def insert_into_table(table, data):
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

def get_country(ip_address):

    country = 'not_found'
    try:
        url = f"https://api.country.is/{ip_address}"
        response = requests.get(url).json()

        if response and 'country' in response:
            country = response['country']
    except Exception as exc:
        print(f"error: {exc}")

    return country

def handler(event, context):

    if IP_ADDRESS not in event:
        return f"{IP_ADDRESS} is absent in event payload"

    ip_address = event[IP_ADDRESS]

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    ip_table = create_table(dynamodb)
    country = get_country(ip_address)

    insert_into_table(
        table=ip_table,
        data=[
                {
                    'ip_address': ip_address,
                    'country': country
                }
            ]
    )

    return f"{ip_address}: {country}"

