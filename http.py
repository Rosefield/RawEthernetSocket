import sys, os, struct, re, traceback, urlparse
#from bs4 import BeautifulSoup

NL = "\n"
CRLF = "\r\n\r\n"

#Construct get request given a URL
def getRequestForURL(url):

    parsed_url = urlparse.urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path

    request = "GET " + (path if (path != None and path != "") else "/") + " HTTP/1.1" + NL + "Host: " + host + CRLF

    return request

#given an http response parse it and write to disk
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

#Write data to disk
def saveData(data, url):

    file = open(getFilenameforURL(url), 'w')
    file.write(data)
    file.close()

#Find filename to write from url
def getFilenameforURL(url):

    path = urlparse.urlparse(url).path

    if path == '/' or path == '':
        return "index.html"
    else:
        return url.split("/")[-1]
