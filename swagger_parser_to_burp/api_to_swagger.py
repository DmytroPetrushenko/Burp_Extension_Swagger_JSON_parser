import requests
import json


def get_swagger_json(gui_object, json_url):
    json_loads = None
    try:
        swagger_response = requests.get(json_url)
        json_loads = json.loads(swagger_response.text)
    except ValueError:
        gui_object.log_area.append('\r\nNo JSON object could be decoded\r\n')
    return json_loads
