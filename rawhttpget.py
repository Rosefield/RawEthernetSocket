import sys, os, socket
import urlparse
import tcp
import struct
import http

url = sys.argv[1]
host_name = urlparse.urlparse(url).hostname

#dest_ip_addr_string = socket.gethostbyname(host_name)

#dest_ip_addr = struct.unpack("!I", socket.inet_aton(dest_ip_addr_string))[0]
#src_ip_addr = struct.unpack("!I", socket.inet_aton(socket.gethostbyname("")))[0]
#Create raw socket
#s = raw_tcp_socket.raw_tcp_socket()

s = tcp.TCPSocket()
s.connect((host_name, 80))

print "connected"

request = http.getRequestForURL(url)

print "http request created"

s.send(request)

print "sent"

response = s.recvall()

print "received response"

http.saveResponse(response, url)

print "saved response"