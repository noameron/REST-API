from enum import Enum

import boto3 as b3


class DB(Enum):
    TABLE_NAME = 'customer_ids'

    
def get_dynamodb_resource():
    return b3.resource('dynamodb')


def put_customer_id(customer_id):
    table = get_dynamodb_resource().Table(DB.TABLE_NAME.value)
    response = table.put_item(Item={'id': customer_id})
    return response


def get_customer_id(customer_id):
    table = get_dynamodb_resource().Table(DB.TABLE_NAME.value)
    response = table.get_item(Key={'id': customer_id})
    return 'id' in response.get('Item', {})



