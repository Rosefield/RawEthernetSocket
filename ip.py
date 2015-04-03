import sys, os
import struct
import utils
import socket
import ethernet

#Need to keep track of state for the Identification field and fragment offset

'''
Header is of the form
 0                   1                   2                   3  
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

class IPHeader:

    def __init__(self, source_address, dest_address):

        self.ihl = 5
        self.type_of_service = 0
        self.total_length = 0
        self.id = 0
        self.fragmentation_offset = 0
        self.ttl = 255
        self.protocol = socket.IPPROTO_TCP
        self.checksum = 0
        self.source_address = source_address
        self.dest_address = dest_address


    def __init__(self, data):

        unpacked = struct.unpack('!BBHHHBBHLL' , data)
        self.ihl = unpacked[0]
        self.type_of_service = unpacked[1]
        self.total_length = unpacked[2]
        self.id = unpacked[3]
        self.fragmentation_offset = unpacked[4]
        self.ttl = unpacked[5]
        self.protocol = unpacked[6]
        self.checksum = unpacked[7]
        self.source_address = unpacked[8]
        self.dest_address = unpacked[9]

    def to_data():
        return struct.pack('!BBHHHBBHLL' , self.ihl, self.type_of_service, self.total_length, self.id, self.fragmentation_offset, self.ttl, self.protocol, self.checksum, self.source_address, self.dest_address)


#Does not deal with receiving/sending fragments
class IPSocket(ethernet.EthernetSocket):
    def __init__(self):
	#horrible hack to get self ip since ubuntu resolves socket.gethostname() to 127.0.0.1
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	self.src_ip = s.getsockname()[0]
	self.src_ip = struct.unpack("!I", socket.inet_aton(self.src_ip))[0]
	
	#self.recv_sock.bind((self.src_ip, 0))
	#self.send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	self.id = 18
	self.dest_ip = ""

	super(IPSocket, self).__init__()


    #Header always 20 Bytes as no options are used
    #Assuming len(data) <= 1480
    def makeIpHeader(self, data):
	Version = 0b0100 #ipv4
	IHL = 0b0101 #size of header in 4byte words
	Type = 0x00
	TotalLen = len(data) + 20
	ID = self.id
	Flags = 0b000
	FragmentOffset = 0
	TTL = 0xFF
	Protocol = 0x06 #TCP
	SourceAddr = self.src_ip
	DestAddr = self.dest_ip

	#fmt = (network order) byte, byte, short
	header = struct.pack("!BBH", (Version << 4) + IHL, Type, TotalLen) 
	header += struct.pack("!HH", ID, (Flags << 13) + FragmentOffset)
	header += struct.pack("!BBH", TTL, Protocol, 0x0)
	header += struct.pack("!LL", SourceAddr, DestAddr)

	checksum = struct.pack("H", utils.calcIpChecksum(header))

	header = header[:10] + checksum + header[12:20]

	calc_checksum = utils.calcIpChecksum(header)
	if calc_checksum != 0:
	    print "checksum calculated incorrectly: ", checksum, calc_checksum

	return header

    def makeIpPacket(self, data):
	header = self.makeIpHeader(data)
	packet = header + data

	return packet

    def validIpPacket(self, header):
	checksum = utils.calcIpChecksum(header)
	if checksum != 0:
	    print checksum
	    return False    

	#print packet
	header = IPHeader(header)
	if header.dest_address != self.src_ip or header.source_address != self.dest_ip:
	 #   print socket.inet_ntoa(struct.pack("!L",header.dest_address)), socket.inet_ntoa(struct.pack("!L", header.source_address))
	    return False


	return True
	

    def send(self, data):
	if len(data) > 1480:
	   pass
	    #fragment
	
	packet = self.makeIpPacket(data)

	self.id += 1
	self.id %= 65536

	return super(IPSocket, self).send(packet)

	#return self.send_sock.sendto(packet, (str(self.dest_ip), 0))

    def recv(self, bufsize):
	data = None

	while data == None:
	    packet = super(IPSocket, self).recv(65536)
	    header = packet[:20]
	    if self.validIpPacket(header):
		header = IPHeader(header)
		#remove any possible trailing ethernet padding
		data = packet[20: header.total_length]
	
	return data

    def connect(self, dest_ip):
	

	self.dest_ip = struct.unpack("!I", socket.inet_aton(dest_ip))[0]
	#IP needed for arp
	super(IPSocket, self).connect(self.src_ip)
	return

    def extractIpHeader(self, data):
	return data[:20]

    def extractIpData(self, data):
	return data[20:]

    #TODO: implement function to close socket
    def close(self):


	super(IPSocket, self).close()

	return
