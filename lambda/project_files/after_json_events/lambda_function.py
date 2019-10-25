import json
import boto3

def lambda_handler(event, context):
    input_body = json.loads(event['body'])
    name = input_body['name']
    number = input_body['number']
    sns = boto3.client(
        'sns',
        region_name='us-east-1',
        aws_access_key_id='***REMOVED_AWS_ACCESS_KEY***',
        aws_secret_access_key='***REMOVED_AWS_SECRET_KEY***'
    )
    resp = sns.publish(
        PhoneNumber=f"+1{str(number)}",
        Message=f"""
                        Dear {name}.
                        Your account has been successfully created on PUTBOX, A NEW WAY FOR ALL YOUR STORAGE!!!
                        """)
    print(resp) # saved in Cloudwatch

    return_body = {
        "body": json.dumps(resp)
    }
    return return_body