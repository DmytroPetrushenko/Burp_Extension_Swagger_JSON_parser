import parser_json
from constant import *
from burp import IBurpExtender, IHttpRequestResponse, IHttpService, ITab
from gui import BurpGui
import datetime


# A BurpExtender class that will interact with the Burp API
class BurpExtender(IBurpExtender, ITab):

    def __init__(self):
        self.callbacks = None
        self.gui = None

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.callbacks.setExtensionName("Parse SwaggerJson to SiteMap")
        self.gui = BurpGui(self)
        self.callbacks.addSuiteTab(self.gui)
        self.gui.log_area.append('\r\nReady to parse!!\r\n')

    # This method transforms the dictionary obtained from JSON into the required data type for the add_to_site_map
    # method
    def create_site_map(self, swagger_dict, json_url, authorization):
        if swagger_dict is not None:
            self.gui.set_log(str(datetime.datetime.now()) + '  ***********  JSON was loaded to parser!\n')
        else:
            return
        parsed_json_dict = parser_json.transform_dir_httprequest(self.gui, swagger_dict, json_url, authorization)
        if parsed_json_dict == EXIT:
            self.gui.set_log('\n\n' + str(datetime.datetime.now())
                             + '  *********** The PARSING was canceled by you!\n\n')
        host = parsed_json_dict.get('host')
        requests = parsed_json_dict.get('requests')
        for http_scheme in parsed_json_dict.get('http_schemes'):
            http_service = HttpService(http_scheme, host)
            for request in requests:
                self.gui.set_log('\n\n' + str(datetime.datetime.now()) + ':\n'
                                 + '  <--------------------begin-------------------->\n'
                                 + request
                                 + '  <---------------------end--------------------->\n')
                self.add_to_site_map(http_service, request, '')

    # A method that creates a SiteMap in Burp Suite
    def add_to_site_map(self, http_service, request, response):
        request_response = HttpRequestResponse(request, response, http_service, "", "")
        self.callbacks.addToSiteMap(request_response)


# Custom class inherited from IHttpService, needed to create SiteMap in Burp Suite
class HttpService(IHttpService):

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


# Custom class inherited from IHttpRequestResponse, needed to create SiteMap in Burp Suite
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
