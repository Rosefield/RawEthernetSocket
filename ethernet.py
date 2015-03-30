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

	#self.dest_mac = self.broadcast_mac
	self.dest_mac = "\x00\x50\x56\xc0\x00\x08"
	#self.dest_mac = "\x00\x00\x00\x00\x00\x00"
	self.src_mac = struct.pack("!Q", uuid.getnode())[2:]

	#For my arch machine, use eth0 for everything else
	self.interface = "ens33"

	self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, EthernetSocket.ETH_P_ALL)
	return

    def send(self, data, eth_type = 0x0800):
	header = struct.pack("!6s6sH", self.dest_mac, self.src_mac, eth_type)
	#pack to minimum length
	if len(data) < 46:
	    data += "\x00"*(46 - len(data))
	
	packet = header + data

	self.socket.sendto(packet, (self.interface,0))
	return

    def recv(self, bufsize):
	data = None

	while data == None:
	    packet = self.socket.recv(65536)
	    if isValid(packet):
		data = packet[14:]

	return data

    def isValid(self, packet):
	unpacked = struct.unpack("!6s6sH", packet[:14])
	dest_mac = unpacked[0]
	src_mac = unpacked[1]
	eth_type = unpacked[2]

	if self.src_mac != dest_mac:
	    return False

	if self.dest_mac != src_mac:
	    return False

	if eth_type != EthernetSocket.ETH_P_IP or eth_type != EthernetSocket.ETH_P_ARP:
	    return False

	return True


    #TODO: Implement ARP
    def connect(self):
	#arp to find gateway

	return
	



