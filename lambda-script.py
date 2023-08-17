import boto3
import json

# Initialize the Boto3 clients for S3 and DynamoDB
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Retrieve the S3 bucket and object key from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_object_key = event['Records'][0]['s3']['object']['key']
    
    # Read the content of the S3 object
    s3_response = s3_client.get_object(Bucket=s3_bucket, Key=s3_object_key)
    s3_content = s3_response['Body'].read().decode('utf-8')
    
    # Parse the JSON content
    data = json.loads(s3_content)
    
    # DynamoDB table name
    dynamodb_table_name = 'YourDynamoDBTableName'
    
    # Write data to DynamoDB
    dynamodb_response = dynamodb_client.put_item(
        TableName=dynamodb_table_name,
        Item={
            'id': {'S': data['id']},
            'attribute1': {'S': data['attribute1']},
            'attribute2': {'N': str(data['attribute2'])}
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data written to DynamoDB successfully')
    }