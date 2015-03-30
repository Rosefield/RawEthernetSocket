import struct
import socket
import uuid

class EthernetSocket(object):
    ETH_P_IP = 0x0800
    ETH_P_ARP = 0x0806
    ETH_P_ALL = 0x0003

    def __init__(self):
	#self.send_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_RAW)

	self.broadcast_mac = "\xff\xff\xff\xff\xff\xff"

	self.dest_mac = self.broadcast_mac
	#self.dest_mac = "\x00\x50\x56\xe8\xa2\x59"
	self.src_mac = struct.pack("!Q", uuid.getnode())[2:]

	#For my arch machine, use eth0 for everything else
	self.interface = "ens33"

	self.send_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(EthernetSocket.ETH_P_ALL))
	self.recv_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(EthernetSocket.ETH_P_ALL))
	return

    def send(self, data, eth_type = 0x0800):
	header = struct.pack("!6s6sH", self.dest_mac, self.src_mac, eth_type)
	#pack to minimum length
	if len(data) < 46:
	    data += "\x00"*(46 - len(data))
	
	packet = header + data

	self.send_sock.sendto(packet, (self.interface,0))
	return

    def recv(self, bufsize, eth_type = 0x0800):
	data = None

	while data == None:
	    packet = self.recv_sock.recv(65536)
	    if EthernetSocket.isValid(self, packet, eth_type):
		data = packet[14:]

	return data

    def isValid(self, packet, desired_type):
	unpacked = struct.unpack("!6s6sH", packet[:14])
	dest_mac = unpacked[0]
	src_mac = unpacked[1]
	eth_type = unpacked[2]

	if eth_type != desired_type:
	    return False

	if self.src_mac != dest_mac:
	    return False


	#If we are still arping, we don't have a dest_mac set yet
	if desired_type != EthernetSocket.ETH_P_ARP:
	    if self.dest_mac != src_mac:
		return False


	return True

    #from stackoverflow.com/questions/2761829/python-get-default-gateway-for-a-local-interface-ip-address-in-linux
    def get_default_gateway(self):
	f = open("/proc/net/route")

	for line in f:
	    fields = line.strip().split()
	    if fields[0] != self.interface or fields[1] != '00000000' or not int(fields[3], 16) & 2:
		continue;

	    return fields[2]

    #TODO: Implement ARP
    def connect(self, src_ip):
	#arp to find gateway

	request = ArpPacket()
	request.SHA = self.src_mac
	request.SPA = src_ip
	request.TPA = socket.htonl(int(self.get_default_gateway(), 16))


	EthernetSocket.send(self, request.toData(), eth_type = EthernetSocket.ETH_P_ARP)

	reply = None
	while reply == None:
	    packet = EthernetSocket.recv(self, 1500, eth_type = EthernetSocket.ETH_P_ARP)
	    packet = ArpPacket(packet)
	    if packet.operation == 2 and packet.THA == self.src_mac and packet.TPA == src_ip:
		reply = packet


	self.dest_mac = reply.SHA

	return


    def close(self):
	self.recv_sock.close()
	self.send_sock.close()
	return

class ArpPacket(object):

    def __init__(self, data = None):
	#Create a request
	if data == None:
	    self.HTYPE = 1 #specify ethernet protocol
	    self.PTYPE = EthernetSocket.ETH_P_IP #type of protocol we want to find out about
	    self.HLEN = 6 #length of ethernet address
	    self.PLEN = 4 #length of ip address
	    self.operation = 1 #1 for request, 2 for reply
	    self.SHA = "\x00\x00\x00\x00\x00\x00" #sender hardware address
	    self.SPA = 0 #ip addr as int
	    self.THA = "\x00\x00\x00\x00\x00\x00" #target hardware address, doesn't matter for request
	    self.TPA = 0 #target protocol address, address to lookup in request
	else:
	    unpacked = struct.unpack("!HHBBHLL", data[:8] + data[14:18] + data[24:28])
	    self.HTYPE = unpacked[0] #specify ethernet protocol
	    self.PTYPE = unpacked[1] #type of protocol we want to find out about
	    self.HLEN = unpacked[2] #length of ethernet address
	    self.PLEN = unpacked[3] #length of ip address
	    self.operation = unpacked[4] #1 for request, 2 for reply, should be 2
	    self.SHA = data[8:14] #Address of host we are looking for
	    self.SPA = unpacked[5] #ip of who sent the reply
	    self.THA = data[18:24] #Address of intended receiver, should be us
	    self.TPA = unpacked[6] #ip of intended receiver, should be us

    def toData(self):
	#data = struct.pack("!HHBBH", self.HTYPE, self.PTYPE, self.HLEN, self.PLEN, self.operation)
	#data += self.SHA
	#data += struct.pack("!L", self.SPA)
	#data += self.THA
	#data += struct.pack("!L", self.TPA)
	data = struct.pack("!HHBBH6sL6sL", self.HTYPE, self.PTYPE, self.HLEN, self.PLEN, self.operation,
			self.SHA, self.SPA, self.THA, self.TPA)

	return data
