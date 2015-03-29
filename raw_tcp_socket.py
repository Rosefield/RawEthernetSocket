import socket, struct
import tcp, ip


class raw_tcp_socket:
    def __init__(self):
	
	

	self.src_port = 51000

	self.dest_ip = ""
	self.dest_port = 0
	#self.data = ""

	self.tcp = ""
	self.ip = ""

    def connect(self, address):
	print address
	host, port = address
	self.dest_ip = socket.gethostbyname(host)
	self.dest_ip = struct.unpack("!I", socket.inet_aton(self.dest_ip))[0]
	self.dest_port = port
	self.tcp = tcp.TCP(self.src_port, self.dest_port)
	self.ip = ip.IP(self.src_ip, self.dest_ip)

	self.tcp.startHandshake()


	return

    def send(self, data):
	packet = self.tcp.makeTcpPacket(data)

	self.addIpHeaderAndSend(packet)

    def addIpHeaderAndSend(self, packet):
	packet = ip.makeIpPacket(packet)

	self.send_sock.sendto(packet, (self.dest_ip, 0))
	return


    def recv(self, bufsize):
	data = None

	while data == None:
	    packet = self.recv_sock.recvfrom(65536)
	    if ip.validIpPacket(self.src_ip, packet):
		ip.parseIpPacket(packet)
		packet = ip.getNextIpPacket()
		if packet != None:
		    if tcp.validTcpPacket(packet):
			tcp.parseTcpPacket(packet)
			data = tcp.getNextTcpPacket()

	return data
    








