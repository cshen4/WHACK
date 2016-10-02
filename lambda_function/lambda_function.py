'''
Twilio Ingest Lambda handler code


'''

import boto3
import random
import StringIO
import urllib2

from boto3.dynamodb.conditions import Key
from boto3.session import Session
from twilio.rest import TwilioRestClient

from cli import *

# create Twilio session
# Add Twilio Keys
account_sid = "AC3af4bdae50407788d5c400e476515950"
auth_token = "65d12dd7f3b0100dec3f0c1e9a4eb9dd"
client = TwilioRestClient(account_sid, auth_token)

# create an S3 & Dynamo session
s3 = boto3.resource('s3')
session = Session()
# Add Dynamo Region and Table
#table_users = dynamodb.Table('table_name')

def sku_dict():
    d = {}
    q = query_db("SELECT SKU from product_database")
    for code in q:
        d.update({q[code]:0})

def lambda_handler(event, context):
    d = sku_dict()

    message = event['body']

    count = 0
    c = ''
    for el in message.split():
        if el.isdigit():
            count = int(el)
        if el in d:
            c = el
    query_db("UPDATE product_database SET Inventory1 = " + count + " WHERE SKU = 'c'")

    from_number = event['fromNumber']


    # check if we have their number
    #response_dynamo
    #table_users.query(KeyConditionExpression=Key('fromNumber').eq(from_number))
    # twilio_resp = 'Thank you for your message.'
    twilio_resp = c + " " + count
    return twilio_resp
