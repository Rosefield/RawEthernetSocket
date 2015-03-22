import sys, os, socket
import urlparse
import ip
import struct






localhost = socket.gethostbyname(socket.gethostname())




url = sys.argv[1]
host_name = urlparse.urlparse(url).hostname

dest_ip_addr_string = socket.gethostbyname(host_name)

dest_ip_addr = struct.unpack("!I", socket.inet_aton(dest_ip_addr_string))[0]
src_ip_addr = struct.unpack("!I", socket.inet_aton(localhost))[0]
#Create raw socket
recv_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
#Bind to host device

#For AF_INET
#recv_sock.bind((localhost, 0))
#for AF_PACKET
recv_sock.bind(("ens33", 0))

send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

data = "A"*20
tcp_packet = tcp.makeTcpPacket(src_port, dest_port, data)
packet = ip.makeIpPacket(src_ip_addr, dest_ip_addr, tcp_packet)

print packet

send_sock.sendto(packet, (dest_ip_addr_string, 0))

packet = recv_sock.recvfrom(65536)
print packet


