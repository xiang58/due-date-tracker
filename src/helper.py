import boto3
import streamlit as st


def get_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb', region_name='us-east-1', 
        aws_access_key_id=st.secrets['aws_access_key_id'],
        aws_secret_access_key=st.secrets['aws_secret_access_key']
    )
    return dynamodb.Table('due-date-tracker')


def get_all_recs():
    table = get_dynamodb_table()
    response = table.scan()
    items = response['Items']
    items.sort(key=lambda x: x['period'])
    return items


def update_reset_dt(rec, new_reset_dt):
    table = get_dynamodb_table()
    response = table.update_item(
        Key={'id': rec['id']},
        UpdateExpression='SET reset_dt = :val',
        ExpressionAttributeValues={':val': new_reset_dt}
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        st.toast('Item inserted successfully!', icon='🎉')
    else:
        st.toast('Error inserting item:' + str(response), icon='🚨')
