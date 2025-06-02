import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = 'oscars-project-bucket'

def lambda_handler(event, context):
    filename = event['queryStringParameters']['filename']
    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': filename, 'ContentType': 'application/octet-stream'},
        ExpiresIn=3600
    )
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': f'{{"url": "{presigned_url}"}}'
    }
