import json
import requests


def lambda_message_sns(name, number):
    url = "https://f4y02mono1.execute-api.us-west-1.amazonaws.com/beta/v1/darshan/putbox/sns"

    payload = {"name": name,
               "number":number}
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)