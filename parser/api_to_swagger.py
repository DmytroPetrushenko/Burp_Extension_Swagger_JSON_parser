import datetime
import json
import requests


def get_swagger_json(gui, json_url):
    json_loads = None
    try:
        swagger_response = requests.get(json_url)
        json_loads = json.loads(swagger_response.text)
    except ValueError:
        gui.set_log('\n' + str(datetime.datetime.now()) + '  ***********  '
                                                       + 'No JSON object could be decoded\n')
    except requests.ConnectionError:
        gui.set_log('\n' + str(datetime.datetime.now()) + '  ***********  '
                    + 'Some kind of error in the URL!!!\n')
    return json_loads
