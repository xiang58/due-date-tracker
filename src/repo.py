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


def edit_rec(rec, new_desc, new_period):
    update_expr = 'SET '
    expression_values = {}

    if new_desc:
        update_expr += 'desc = :desc,'
        expression_values[':desc'] = new_desc
    if new_period:
        update_expr += 'period = :period,'
        expression_values[':period'] = new_period
    if update_expr.endswith(','):
        update_expr = update_expr[:-1]

    table = get_dynamodb_table()
    response = table.update_item(
        Key={'id': rec['id']},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_values
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        st.toast('Item updated successfully!', icon='🎉')
    else:
        st.toast('Error updating item:' + str(response), icon='🚨')


def add_rec(num_recs, desc, period, reset_dt):
    table = get_dynamodb_table()
    rec = {
        'id': num_recs + 1,
        'desc': desc,
        'period': period,
        'reset_dt': reset_dt
    }
    response = table.put_item(Item=rec)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        st.toast('Item added successfully!', icon='🎉')
    else:
        st.toast('Error adding item:' + str(response), icon='🚨')
