import parser.parser_json as debug
import requests as re
import json


swagger_response = re.get('https://petstore.swagger.io/v2/swagger.json')
json_loads = json.loads(swagger_response.text)
debug.transform_dir_httprequest(json_loads)