import requests
import json


def get_swagger_json(json_url):
    swagger_response = requests.get(json_url)
    return json.loads(swagger_response.text)
