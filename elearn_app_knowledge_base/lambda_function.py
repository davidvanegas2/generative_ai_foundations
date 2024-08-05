"""Lambda function to access the foundational model using the knowledge base API."""

import boto3

bedrock = boto3.client('bedrock-agent-runtime')


def lambda_handler(event, context):
    """Lambda handler to access the foundational model using the knowledge base API."""
    user_prompt = event['prompt']
    response = bedrock.retrieve_and_generate(
        input={'text': user_prompt},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'UBOCLDWDCM',
                'modelArn': 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-v2:1'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': response['output']['text']
    }
