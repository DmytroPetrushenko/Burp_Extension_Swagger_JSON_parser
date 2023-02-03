CONTENT_TYPE_DEFAULT = 'application/json'
CONTENT_TYPE = 'Content-Type'
POST = 'POST'
PUT = 'PUT'
PATHS = 'paths'
BASE_PATH = 'basePath'
HOST = 'host'
DICT = {
        'integer': {'default': 100500, 'int32': 0, 'int64': 1},
        'string': {'default': 'STRING', 'date': '2023-01-19', 'date-time': '2023-01-19T16:57:08.404Z',
                   'password': 'password', 'uuid': 'UUID'},
        'number': {'default': 100500.0, 'float': 0.100500, 'double': 1.100500},
        'boolean': {'default': 'true'},
        'object': {'default': '{"JSON":"OBJECT"}'},
        'file': {'default': 'SOME_FILE'}
        }
BOUNDARY = '---------------------------162414598940203848951676920930'
