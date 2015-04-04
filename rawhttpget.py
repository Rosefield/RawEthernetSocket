import sys, os, socket
import urlparse
import tcp
import struct
import http

url = sys.argv[1]
host_name = urlparse.urlparse(url).hostname

#Construct our socket
s = tcp.TCPSocket()
#Connect to the remote host
s.connect((host_name, 80))

#Create request
request = http.getRequestForURL(url)

#Send request to host
s.send(request)

#Get all data from the request
response = s.recvall()

#Save data to disk
http.saveResponse(response, url)

#Close the socket
s.close()
