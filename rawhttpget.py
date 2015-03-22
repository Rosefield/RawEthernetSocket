import sys, os, socket
import urlparse
import ip
import struct





url = sys.argv[1]
host_name = urlparse.urlparse(url).hostname

dest_ip_addr_string = socket.gethostbyname(host_name)

dest_ip_addr = struct.unpack("!I", socket.inet_aton(dest_ip_addr_string))[0]
src_ip_addr = struct.unpack("!I", socket.inet_aton(localhost))[0]
#Create raw socket
s = raw_tcp_socket()
s.connect((host_name, 80))

data = "A"*20

s.send(data)

packet = s.recv(1500)
print packet


