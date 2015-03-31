import sys, os, struct, re, traceback 
from bs4 import BeautifulSoup

CRLF = "\r\n\r\n"

class HTTPGet(object):

    def __init__(self, url):

        self.url = url

    def execute(self):

        parsed_url = urlparse.urlparse(self.url)

        request = 'GET ' + parsed_url.path + ' HTTP/1.1' + NL
        request += "Host: " + parsed_url.hostname + CRLF
        data = makeRequest(url, request)

        TCP.sendHTTPRequest(request)

    def recieveHTTPResponse(self, http_response):

        if getStatusCode(http_response) == 200:
            saveData(http_response)
        else:
            throwError()

    def getStatusCode(self, http_response):

        try:
            return int(re.search("HTTP/1.1\s(\d+)\s", data).group(1))
        except AttributeError:
            throwError()

    def getBody(self, http_response):

        crlf_position = http_reply.find(CRLF)
        return http_response[(crlf_position + 4):]

    def throwError(self):

        print "An error occured."
        traceback.print_exc()
        sys.exit()

    def saveData(self, data):

        file = open(getFilename(), 'w')
        file.write(data)
        file.close()

    def getFilename(self):

        if self.url[-1] == '/':
            return "index.html"
        else:
            return self.url.split("/")[-1]
