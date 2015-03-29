import sys, os, struct
import utils

class TCPHeader:

    def __init__(self, src_port, dest_port, seq, ack_seq, window, syn, fin, ack):

	self.src_port = src_port   # source port
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


    def to_data(self):

        return struct.pack('!HHLLHHHH' , self.src_port, self.dest_port, self.seq, self.ack_seq, (self.data_offset << 12) + (self.ack << 4) + (self.syn << 1) + self.fin, self.window, self.checksum, self.urgent_pointer)



#Implement TCP Stack
class TCP:

    def __init__(self, src_addr, src_port, dest_addr, dest_port):
	
	#State information
	self.seq = 0
	self.ack_seq = 0
	self.window_size = 65535
	self.send_window = []
	self.recv_window = []
	#set to 0 until after handshake
	self.syn = 1
	#set to 1 when we want to teardown the connection
	self.fin = 0
	#set to 1 after handshake
	self.ack = 0
	self.src_addr = src_addr
	self.src_port = src_port
	self.dest_addr = dest_addr
	self.dest_port = dest_port

    

    def makeTcpHeader(self, data):
	header = TCPHeader(self.src_port, self.dest_port, self.seq, self.ack_seq, self.window_size, self.syn, self.fin, self.ack).to_data()

	self.seq += 20 + len(data)

	psh = struct.pack("!LLBBH", self.src_addr, self.dest_addr, 0, 0x6, 20 + len(data))

	checksum = struct.pack("H", utils.calcIpChecksum(psh + header + data))

	print "calculated checksum: ", hex(utils.calcIpChecksum(psh + header + data))


	header = header[:16] + checksum + header[18:20]

	check = utils.calcIpChecksum(psh + header + data)
	if check != 0:
	    print "incorrect tcp checksum: ", hex(check), checksum

	return header

    def makeTcpPacket(self, data):
	header = self.makeTcpHeader(data)
	packet = header + data

	return packet

    def startHandshake(self):
	

	return


    def extractTcpHeader(self, packet):
	return packet[:20]    

    def extractTcpPacket(self, packet):
	return packet[20:]
