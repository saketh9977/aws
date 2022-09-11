import boto3

import time
import json

ATHENA_DB = 'saketh_test_db'
ATHENA_QUERY_OUT_S3 = 's3://quadrant-ftest2/saketh/athena-wg-saketh-test-query-results/'
ATHENA_REGION = 'us-east-1'

def exponential_backoff(client, query_start):
    retry_num = 0
    while True:

        query_execution = client.get_query_execution(
            QueryExecutionId=query_start['QueryExecutionId']
        )

        sleep_time = int((2 ** retry_num) / 1000)
        print(f'exponential backoff: sleeping for {sleep_time}s')
        time.sleep(sleep_time)

        query_state = query_execution['QueryExecution']['Status']['State']
        if (query_state.lower() in ['queued', 'running']) == False:
            # print(json.dumps(query_execution, indent=4, default=str))
            print(f"exponential backoff: query state = {query_state}")
            break

        retry_num = retry_num + 1

def execute_athena_query(sql_file):
    client = boto3.client('athena', region_name=ATHENA_REGION)

    with open(sql_file, 'r') as f_stream:
        sql_string = f_stream.read()

    query_start = client.start_query_execution(
        QueryString = sql_string,
        QueryExecutionContext = {
            'Database': ATHENA_DB
        }, 
        ResultConfiguration = { 'OutputLocation': ATHENA_QUERY_OUT_S3 }
    )

    exponential_backoff(client, query_start)
        

def main():
    SQL_FILE = './sql/create-athena-table.sql'
    execute_athena_query(SQL_FILE)

    SQL_FILE = './sql/query-athena-table.sql'
    execute_athena_query(SQL_FILE)

if __name__ == '__main__':
    main()