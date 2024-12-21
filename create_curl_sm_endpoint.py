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
    "input": ["Sample text 1", "Sample text 2"],
    "input_type": "query",
    "truncation": "true"
}

# Construct an AWS Request to sign
aws_request = AWSRequest('POST', url, data=json.dumps(payload))

# Sign the AWS Request
SigV4Auth(session.get_credentials(), SERVICE, REGION).add_auth(aws_request)

# Get prepared request header
headers = aws_request.prepare().headers

# Create header flags
header_flags = ' '.join([f"-H '{key}: {value}'" for key, value in headers.items()])

# Print out curl command
print(f"curl --request POST --url {url} -H 'Content-Type: application/json' {header_flags} -d '{json.dumps(payload)}'")
