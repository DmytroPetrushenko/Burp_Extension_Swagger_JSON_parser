from constant import CONTENT_TYPE_DEFAULT, CONTENT_TYPE, POST, PUT, PATHS, BASE_PATH, HOST, DICT, BOUNDARY

definitions = {}

def transform_dir_httprequest(swagger_dict):
    requests = []
    paths = swagger_dict.get(PATHS)
    base_path = swagger_dict.get(BASE_PATH)
    host = swagger_dict.get(HOST)
    http_schemes = swagger_dict.get('schemes')
    definitions.update(swagger_dict.get('definitions'))
    for path_name, path_data in paths.items():
        for http_method_name, http_method_data in path_data.items():
            requests.append(create_http_request(base_path + path_name, host, http_method_name, http_method_data))
    return {'requests': requests, HOST: host, 'http_schemes': http_schemes}


def convert_json_value(parameter):
    type_value = parameter.get('type')
    format_value = parameter.get('format')
    example_value = parameter.get('example')
    enum_value = parameter.get('enum')

    if enum_value is not None:
        default_enum_value = enum_value[0]
        return '\"' + default_enum_value + '\"' if type_value == 'string' else default_enum_value

    if type_value == 'string' and example_value is not None:
        return '\"' + example_value + '\"'

    if (type_value == 'string' or type_value == 'boolean') and format_value is None:
        str_bool_value = DICT.get(type_value).get('default')
        return '\"' + str_bool_value + '\"' if type_value == 'string' else str_bool_value

    if type_value == 'string' and format_value is not None:
        return '\"' + DICT.get(type_value).get(format_value) + '\"'

    if type_value == 'file' and format_value is None:
        return '\"' + DICT.get(type_value) + '\"'

    if type_value == 'array':
        return '[' + convert_json_value(parameter.get('items')) + ']'

    if parameter.get('$ref') is not None:
        return create_json_body(parameter)

    return str(DICT.get(type_value).get(format_value))


def create_content_type(http_method_data):
    content_type_summary = CONTENT_TYPE + ': '
    content_type_list = http_method_data.get('consumes')
    if content_type_list is None:
        return ''
    if CONTENT_TYPE_DEFAULT in content_type_list:
        content_type_summary += CONTENT_TYPE_DEFAULT
    else:
        content_type_summary += content_type_list[0]
    content_type_summary += '; boundary=' + BOUNDARY if 'multipart/form-data' in content_type_list else ''
    return content_type_summary + '\r\n'


def create_content_length(http_method_name):
    if http_method_name.upper() in [POST, PUT]:
        return 'Content-Length: 1' + '\r\n\r\n'
    return ''


def create_accept(http_method_data):
    accept_summary = 'Accept: '
    accept_list = http_method_data.get('produces')
    list_length = len(accept_list)
    for index in range(list_length):
        if list_length - 1 == index:
            accept_summary += accept_list[index]
        else:
            accept_summary += accept_list[index] + ', '
    return accept_summary + '\r\n'


def create_form_data_upload_body(parameter, boundary):
    name = parameter.get('name')
    file_name = '; filename=\"wolf_head.png\"' + '\r\n' + CONTENT_TYPE + ': image/png' if name == 'file' else ''
    form_data_body = 'Content-Disposition: form-data; name=\"' + name + '\"' + file_name + '\r\n\r\n' \
                     + convert_json_value(parameter).replace('\"', '') + '\r\n' \
                     + boundary
    return form_data_body


def create_form_data_body(parameter):
    return parameter.get('name') + '=' + convert_json_value(parameter)


def create_json_body(schema):
    result = '{'
    schema_definitions = schema.get('$ref').split('/')[2]
    object_properties = definitions.get(schema_definitions).get('properties')
    for name, value in object_properties.items():
        if result != '{':
            result += ', '
        if len(value) == 1 and '$ref' in value.keys():
            result += '\"' + name + '\": ' + create_json_body(value)
        else:
            result += '\"' + name + '\": ' + convert_json_value(value)
    return result + '}'


def create_query(parameter):
    items = parameter.get('items')
    return parameter.get('name') + '=' + convert_json_value(items if items is not None else parameter).replace('\"', '')


def create_http_request(path_name, host, http_method_name, http_method_data):
    http_request_body = ''
    query = ''
    consumes = http_method_data.get('consumes')
    body_parameters = http_method_data.get('parameters')
    length_body_parameters = len(body_parameters)
    for index in range(length_body_parameters):
        parameter = body_parameters[index]
        tag_in = parameter.get('in')
        if tag_in == 'path':
            path_part = convert_json_value(parameter).replace('\"', '')
            path_name = path_name if path_part is None else path_name.replace('{' + parameter.get('name') + '}',
                                                                              path_part)
        if tag_in == 'formData' and 'multipart/form-data' in consumes:
            boundary= '--' + BOUNDARY + ('--' if index == length_body_parameters - 1 else '')
            if http_request_body == '':
                http_request_body += boundary + '\r\n'
            http_request_body += create_form_data_upload_body(parameter, boundary) + '\r\n'

        if tag_in == 'formData' and 'application/x-www-form-urlencoded' in consumes:
            if http_request_body == '':
                http_request_body += create_form_data_body(parameter)
            else:
                http_request_body += '&' + create_form_data_body(parameter)

        if tag_in == 'body':
            schema = parameter.get('schema')
            if schema.get('type') == 'array':
                http_request_body = '[' + create_json_body(schema.get('items')) + ']'
            else:
                http_request_body = create_json_body(schema)

        if tag_in == 'query':
            if query == '':
                query += '?' + create_query(parameter)
            else:
                query += '&' + create_query(parameter)

    http_request_body += '' if http_request_body.endswith('\r\n') or http_request_body == '' else '\r\n'
    http_request_result = http_method_name.upper() + ' ' + path_name + query + ' HTTP/1.1\r\n' \
                          + 'Host: ' + host + '\r\n' \
                          + create_accept(http_method_data) \
                          + create_content_type(http_method_data) \
                          + create_content_length(http_method_name) \
                          + http_request_body + '\r\n'

    # + 'Comment: ' + http_method_data.get('summary') + '\r\n' \
    print(http_request_result)
    return http_request_result