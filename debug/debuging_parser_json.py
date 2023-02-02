import parser.parser_json as debug
import requests as re
import json

json_url = 'https://crm-app-nightly.genci0.eisgroup.com/api/common/schema/v1/activities/swagger.json'
authorization = 'cWE6cWE='
swagger_response = re.get(json_url, headers={'Authorization': 'Basic cWE6cWE='})
json_loads = json.loads(swagger_response.text)
debug.transform_dir_httprequest(json_loads, json_url, authorization)