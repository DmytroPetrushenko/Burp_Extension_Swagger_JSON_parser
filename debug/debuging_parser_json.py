import json
import requests as re
from parser import parser_json


class BurpGui:
    def create_popup_form(self):
        return 'https://dxp-gateway-nwp-pentest.dev.aws08.nwevb.cloud/'


# json_url = 'https://dxp-gateway-nwp-pentest.dev.aws08.nwevb.cloud/swagger.json?apiGroup=All%20APIs'
json_url = 'https://petstore.swagger.io/v2/swagger.json'
# authorization = 'cWE6cWE='
swagger_response = re.get(json_url, headers={'Authorization': 'Basic cWE6cWE='})
print(swagger_response)
json_loads = json.loads(swagger_response.text)
parser_json.transform_dir_httprequest(BurpGui(), json_loads, json_url, '')



