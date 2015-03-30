import sys, os, socket
import urlparse
import tcp
import struct




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


'''
s.send("GET / HTTP/1.1\nHost: david.choffnes.com\r\n\r\n")

print "sent"

packet = s.recv(1500)
print packet

print 'received'
'''
s.close()
print "closed the socket"
