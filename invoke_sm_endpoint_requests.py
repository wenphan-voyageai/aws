import boto3
import json
import requests
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth

PROFILE='wen-dev'
REGION='us-east-2'
SERVICE='sagemaker'
HOST='runtime.sagemaker.us-east-2.amazonaws.com'
ENDPOINT='/endpoints/voyage-3/invocations'

url=f'https://{HOST}{ENDPOINT}'

# Get crendentials into session
session = boto3.Session(profile_name=PROFILE, region_name=REGION)

# Payload
payload = { 
    "input": ['Sample text 1', 'Sample text 2'],
    "input_type": 'query',
    "truncation": 'true'
}

# Construct an AWS Request to sign
aws_request = AWSRequest('POST', url, data=json.dumps(payload))

# Sign the AWS Request
SigV4Auth(session.get_credentials(), SERVICE, REGION).add_auth(aws_request)

# Get prepared request header
headers = aws_request.prepare().headers

# Call SageMaker inference endpoint with standard request
try:
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=5)
    response.raise_for_status()
    print(f'Response Status: {response.status_code}')
    print(f'Response Body: {response.content.decode("utf-8")}')
except Exception as e:
    print(f'Error: {e}')
