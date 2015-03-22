import sys, os, struct

class TCPHeader:

    def __init__(self, source_port, dest_port, seq, ack_seq, window, syn, fin, ack):

		self.source_port = source_port   # source port
		self.dest_port = dest_port
		self.seq = seq
		self.ack_seq = ack_seq
		self.data_offset = 5
		self.fin = fin
		self.syn = syn
		self.rst = 0
		self.psh = 0
		self.ack = ack
		self.urg = 0
		self.window = window
		self.checksum = 0
		self.urgent_pointer = 0

    def __init__(self, data):

        unpacked = unpack('!BBHHHBBH4s4s' , self.ihl, self.type_of_service, self.total_length, self.id, self.fragmentation_offset, self.ttl, self.protocol, self.checksum, self.source_address, self.dest_address)

    def to_data():
        return pack('!BBHHHBBH4s4s' , self.ihl, self.type_of_service, self.total_length, self.id, self.fragmentation_offset, self.ttl, self.protocol, self.checksum, self.source_address, self.dest_address)



#Implement TCP Stack
STATE = 0

def makeTcpHeader(src_port, dest_port, data):

    return

def makeTcpPacket(src_port, dest_port, data):
    header = makeTcpHeader(src_port, dest_port, data)
    packet = header + data

    return packet

def extractTcpHeader(packet):
    return packet[:20]    

def extractTcpPacket(packet):
    return packet[20:]
