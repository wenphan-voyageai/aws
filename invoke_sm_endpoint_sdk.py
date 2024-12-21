import boto3
import json
import requests
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth

PROFILE='wen-dev'
REGION='us-east-2'
MODEL_ENDPOINT_NAME='voyage-3'

# Get crendentials into session
session = boto3.Session(profile_name=PROFILE, region_name=REGION)

# Payload
payload = { 
    "input": ['Sample text 1', 'Sample text 2'],
    "input_type": 'query',
    "truncation": 'true'
}

# Create SageMaker runtime client
sm_runtime = boto3.client("sagemaker-runtime", region_name=REGION)

# Invoke endpoint with SageMaker runtime client
try:
    response = sm_runtime.invoke_endpoint(
        EndpointName=MODEL_ENDPOINT_NAME,
        ContentType="application/json",
        Accept="application/json",
        Body=json.dumps(payload)
    )
    print(json.load(response["Body"]))
except Exception as e:
    print(f'Error: {e}')
