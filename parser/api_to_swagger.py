import datetime
import json
import requests


def get_swagger_json(gui, json_url, authorization):
    json_loads = None
    try:
        gui.set_log('\nAuthorization : Basic ' + authorization + '\n')
        swagger_response = requests.get(json_url, headers={'Authorization': 'Basic ' + authorization})
        json_loads = json.loads(swagger_response.text)
    except ValueError:
        gui.set_log('\n' + str(datetime.datetime.now()) + '  ***********  '
                                                       + 'No JSON object could be decoded\n')
    except requests.ConnectionError:
        gui.set_log('\n' + str(datetime.datetime.now()) + '  ***********  '
                    + 'Some kind of error in the URL!!! Maybe, you should check your VPN connection! '
                    + 'Or something else! \n')
    return json_loads
