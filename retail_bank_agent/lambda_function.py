"""Lambda function responsible to retrieve the data from DynamoDB and return the response to the chatbot."""
import json
import os
from decimal import Decimal

import boto3

DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE', 'customerAccountStatus')
dynamo_db = boto3.resource('dynamodb')


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON."""
    def default(self, obj):
        """Convert decimal to float."""
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def return_response(event, status_code, body):
    """Return the response with the status code and body."""
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event['actionGroup'],
            "apiPath": event['apiPath'],
            "httpMethod": event['httpMethod'],
            "httpStatusCode": status_code,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body, cls=DecimalEncoder)
                }
            }
        },

    }


def lambda_handler(event, context):
    """
    Lambda function responsible to get item from DynamoDB based in Account ID and return the response to the chatbot.
    """
    account_id = event['parameters'][0]['value']
    table = dynamo_db.Table(DYNAMODB_TABLE)
    response = table.get_item(Key={'AccountID': int(account_id)})
    item = response.get('Item', {})

    if not item:
        return return_response(event, 404, 'Account not found.')
    return return_response(event, 200, item)
