import api_to_swagger
import parser_json
from burp import IBurpExtender, IHttpRequestResponse, IHttpService, ITab
from gui import BurpGui


class BurpExtender(IBurpExtender, ITab):

    def __init__(self):
        self.callbacks = None

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.callbacks.setExtensionName("Parse SwaggerJson to SiteMap")
        self.callbacks.addSuiteTab(BurpGui(self))

    def create_site_map(self, swagger_dict):
        # swagger_dict = api_to_swagger.get_swagger_json('https://petstore.swagger.io/v2/swagger.json')
        parsed_json_dict = parser_json.transform_dir_httprequest(swagger_dict)
        host = parsed_json_dict.get('host')
        requests = parsed_json_dict.get('requests')
        for http_scheme in parsed_json_dict.get('http_schemes'):
            http_service = HttpService(http_scheme, host)
            for request in requests:
                self.add_to_site_map(http_service, request, '')

    def add_to_site_map(self, http_service, request, response):
        request_response = HttpRequestResponse(request, response, http_service, "", "")
        self.callbacks.addToSiteMap(request_response)


class HttpService(IHttpService):

    # copied from https://github.com/modzero/burp-ResponseClusterer/blob/master/ResponseClusterer.py
    def __init__(self, http_scheme, host):
        self._protocol = http_scheme
        self._host = host
        if self._protocol == "http":
            self._port = 80
        elif self._protocol == "https":
            self._port = 443

    def getHost(self):
        return self._host

    def getPort(self):
        return self._port

    def getProtocol(self):
        return self._protocol

    def __str__(self):
        return "protocol: {}, host: {}, port: {}".format(self._protocol, self._host, self._port)


class HttpRequestResponse(IHttpRequestResponse):

    def __init__(self, request, response, http_service, cmt, color):
        self.setRequest(request)
        self.setResponse(response)
        self.setHttpService(http_service)
        self.setHighlight(color)
        self.setComment(cmt)

    def getRequest(self):
        return self.req

    def getResponse(self):
        return self.resp

    def getHttpService(self):
        return self.serv

    def getComment(self):
        return self.cmt

    def getHighlight(self):
        return self.color

    def setHighlight(self, color):
        self.color = color

    def setComment(self, cmt):
        self.cmt = cmt

    def setHttpService(self, http_service):
        self.serv = http_service

    def setRequest(self, message):
        self.req = message

    def setResponse(self, message):
        self.resp = message
