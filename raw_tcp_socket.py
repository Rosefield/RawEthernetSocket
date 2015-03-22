import socket, struct
import tcp, ip


class raw_tcp_socket:
    def __init__(self):
	self.recv_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
	self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	
	
	self.recv_sock.bind(("ens33", 0))
	self.send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	self.src_port = 51000
	self.src_ip = socket.gethostbyname(socket.gethostname())

	self.dest_ip = ""
	self.dest_port = 0
	#self.data = ""


    def connect(address):
	host, port = address
	self.dest_ip = socket.gethostbyname(host)\
	self.dest_port = port

	tcp.startHandshake(dest_ip, dest_port)


	return

    def send(data):
	packet = tcp.makeTcpPacket(src_port, dest_ip, data)
	packet = ip.makeIpPacket(src_ip, dest_ip, packet)

	send_sock.sendto(packet, (self.dest_ip, 0))
	return

    def recv(bufsize):
	'''
	if len(self.data) >= 0
	    result = self.data[:bufsize]
	    self.data = self.data[bufsize:]
	    return result	
	'''

	data = None

	while data == None:
	    packet = sock.recvfrom(65536)
	    if ip.validIpPacket(src_ip, packet):
		ip.parseIpPacket(packet)
		packet = ip.getNextIpPacket()
		if packet != None:
		    if tcp.validTcpPacket(src_port, packet):
			tcp.parseTcpPacket(packet)
			data = tcp.getNextTcpPacket()

	return data
    








