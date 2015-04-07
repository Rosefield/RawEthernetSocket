import sys, os, struct, re, traceback, urlparse
from bs4 import BeautifulSoup

NL = "\n"
CRLF = "\r\n\r\n"

def getRequestForURL(url):

    parsed_url = urlparse.urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path

    request = "GET " + (path if (path != None and path != "") else "/") + " HTTP/1.1" + NL + "Host: " + host + CRLF

    return request

def saveResponse(http_response, url):

    if getStatusCode(http_response) == 200:
        body = getBody(http_response)
        saveData(body, url)
    else:
        throwError()

def getStatusCode(http_response):

    try:
        return int(re.search("HTTP/1.1\s(\d+)\s", http_response).group(1))
    except AttributeError:
        throwError()

def getBody(http_response):

    crlf_position = http_response.find(CRLF)
    return http_response[(crlf_position + 4):]

def throwError():

    print "An error occured."
    traceback.print_exc()
    sys.exit()

def saveData(data, url):

    file = open(getFilenameforURL(url), 'w')
    file.write(data)
    file.close()

def getFilenameforURL(url):

    if url[-1] == '/':
        return "index.html"
    else:
        return url.split("/")[-1]
