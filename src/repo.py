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
    expression_names = {}

    if new_desc:
        update_expr += '#desc = :desc,'
        expression_values[':desc'] = new_desc
        expression_names['#desc'] = 'desc'
    if new_period:
        update_expr += '#period = :period,'
        expression_values[':period'] = new_period
        expression_names['#period'] = 'period'
    if update_expr.endswith(','):
        update_expr = update_expr[:-1]

    table = get_dynamodb_table()
    response = table.update_item(
        Key={'id': rec['id']},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        st.toast('Item updated successfully!', icon='🎉')
    else:
        st.toast('Error updating item:' + str(response), icon='🚨')


def add_rec(recs, desc, period, reset_dt):
    table = get_dynamodb_table()
    new_id = max([rec['id'] for rec in recs], default=0) + 1
    
    rec = {
        'id': new_id,
        'desc': desc,
        'period': period,
        'reset_dt': reset_dt
    }
    
    response = table.put_item(Item=rec)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        st.toast('Item added successfully!', icon='🎉')
    else:
        st.toast('Error adding item:' + str(response), icon='🚨')


def del_rec(rec_id):
    table = get_dynamodb_table()
    response = table.delete_item(
        Key={'id': rec_id}
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        st.toast('Item deleted successfully!', icon='🎉')
    else:
        st.toast('Error deleting item:' + str(response), icon='🚨')
