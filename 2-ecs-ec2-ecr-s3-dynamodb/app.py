from src.extractor import (
    extract
)
from src.transformer import (
    get_transformed_response
)
from src.loader import (
    insert_into_dynamodb
)

def etl():
    res_list = extract()
    trans_data = get_transformed_response(res_list)
    insert_into_dynamodb(trans_data)

if __name__ == '__main__':
    etl()