import api_to_swagger
import parser_json

swagger_dict = api_to_swagger.get_swagger_json('https://petstore.swagger.io/v2/swagger.json')
dir_httprequest = parser_json.transform_dir_httprequest(swagger_dict)
for request in dir_httprequest.get('requests'):
    print(request)