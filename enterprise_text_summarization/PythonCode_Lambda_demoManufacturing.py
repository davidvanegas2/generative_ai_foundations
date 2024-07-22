"""
Lambda function to call Bedrock API for text summarization based on reports from manufacturing industry
"""
import json
# 1 Import boto3 and create client connection with bedrock
import boto3

client_bedrock = boto3.client('bedrock-runtime')


def lambda_handler(event, context):
    """
    This function is used to generate a text summary using the Bedrock Service. The input data is the prompt
    :param event: Event is the input data that is passed to the function
    :param context: Context is the runtime information of the function
    :return: Returns the text summary
    """
    # 2 a. Store the input in a variable, b. print the event
    input_prompt = event['prompt']
    print(input_prompt)

    # 3. Create  Request Syntax - Get details from console & body should be json object - use   json.dumps for body

    client_bedrock_request = client_bedrock.invoke_model(
        contentType='application/json',
        accept='application/json',
        modelId='cohere.command-light-text-v14',
        body=json.dumps({
            "prompt": input_prompt,
            "temperature": 0.9,
            "p": 0.75,
            "k": 0,
            "max_tokens": 100}))
    # print(client_bedrock_request)

    # 4. Convert Streaming Body to Byte(.read method) and then Byte to String using json.loads#
    client_bedrock_byte = client_bedrock_request['body'].read()

    # 5 a. Print the event and type , b. Store the input in a variable
    client_bedrock_string = json.loads(client_bedrock_byte)
    # print(client_bedrock_string)

    # 6. Update the 'return' by changing the 'body'
    client_final_response = client_bedrock_string['generations'][0]['text']
    print(client_final_response)

    return {
        'statusCode': 200,
        'body': json.dumps(client_final_response)
    }
