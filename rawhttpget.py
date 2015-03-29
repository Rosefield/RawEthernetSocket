import sys, os, socket
import urlparse
import ip
import tcp
import struct




url = sys.argv[1]
host_name = urlparse.urlparse(url).hostname

dest_ip_addr_string = socket.gethostbyname(host_name)

dest_ip_addr = struct.unpack("!I", socket.inet_aton(dest_ip_addr_string))[0]
#src_ip_addr = struct.unpack("!I", socket.inet_aton(socket.gethostbyname("")))[0]
#Create raw socket
#s = raw_tcp_socket.raw_tcp_socket()
s = ip.IPSocket()
s.connect(dest_ip_addr_string)

tcpstate = tcp.TCP(3232246917, 5100, dest_ip_addr, 80,)
data = ""
packet = tcpstate.makeTcpPacket(data)

s.send(packet)

packet = s.recv(1500)
print packet


