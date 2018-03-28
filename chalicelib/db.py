import uuid

import boto3
from boto3.dynamodb.conditions import Key

def connect_to_db():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('WritersGuild')

    return table

def get_table():
    table = connect_to_db()
    return table

def get_all():
    all_items = get_table().scan()
    result = all_items['Items']

    return result

def get_item(company):
    all_items = get_all()
    for each in all_items:
        if company == each['Company']:
            return each

    return company + " does not exist"

def company_exist(company):
    all_items = get_all()
    # for each in all_items:
    #     company_exist = each['Company']

    if not any(each['Company'] == company for each in all_items):
        return False
    else:
        return True
        # if company == company_exist:
        #     return True
        # else:
        #     return False


def post_item(data):
    get_table().put_item(
        Item={
            'UUID': str(uuid.uuid1()),
            'Company': data['Company'],
            'TeamMembers': data['TeamMembers']
        }
    )

    return "Company added"

def put_item(company, data):
    if not company_exist(company):
        print(company + " does not exist")
        return company + " does not exist"

    item = get_item(company)
    uuid = item['UUID']

    get_table().update_item(
        Key={'UUID': uuid},
        UpdateExpression='SET TeamMembers = :teammembers_value',
        ExpressionAttributeValues={
            ':teammembers_value': data['TeamMembers']
        }     
    )

    print(company + " has been updated")
    return company + " has been updated"

def delete_item(uuid):
    get_table().delete_item(
        Key={'UUID':uuid}
    )