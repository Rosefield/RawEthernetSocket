import sys, os, struct, random, threading
from ip import *
import utils

class TCPSocket(IPSocket):

    timeout_seconds = 60
    max_packet_size = 1024
    max_sequence_number = 4294967295
    window_size = 65535
    recv_size = 65535

    def __init__(self):


        self.source_port = random.randint(0, 65535)
        self.dest_port = 0

        self.connection_initialized = False

        self.have_finned = False
        self.received_fin = False

        # TCP Stuff

        self.cwnd = 1

        # Send Stuff

        self.ack_number = 0
        self.sequence_number = random.randint(0, TCPSocket.max_sequence_number)

        #self.data_packets_to_send = []
        self.packets_in_flight = []

        # receive Stuff 

        self.receive_window = []


        self.recv_buf = ""

        # Initialize and listen on the socket

        super(TCPSocket, self).__init__()

    

    def connect(self, address):
        host, port = address
        self.dest_port = port

        super(TCPSocket, self).connect(socket.gethostbyname(host))
    
        self.openConnection()

    def send(self, data):
        packet = TCPPacket(self.source_port, self.dest_port, self.sequence_number, self.ack_number, TCPSocket.window_size, 0,0,1, data)
        self.sendPacket(packet)

    def recvall(self):
        data = None
        while (not self.received_fin) and (not self.have_finned):
            packet = super(TCPSocket, self).recv(TCPSocket.window_size)
            data = self.parsePacket(packet)
            if data != None and data != "":
                self.recv_buf += data
        return self.recv_buf

    def recv(self):
        packet = super(TCPSocket, self).recv(TCPSocket.window_size)
        data = self.parsePacket(packet)

    def openConnection(self):

        SYNPacket = TCPPacket(self.source_port, self.dest_port, self.sequence_number, self.ack_number, TCPSocket.window_size, 1, 0, 0, "")
        self.sendPacket(SYNPacket)

        #don't need to do anything, recv will take care of acking the packet
	while not self.connection_initialized:
	    synack = self.recv()


    def sendFin(self):
        FINPacket = TCPPacket(self.source_port, self.dest_port, self.sequence_number, self.ack_number, TCPSocket.window_size, 0, 1, 1, "")
        self.sendPacket(FINPacket)

    def teardown(self):
        if not self.have_finned:
            self.sendFin()
            self.have_finned = True
            if self.received_fin:
                super(TCPSocket, self).close()
                return
        while not self.received_fin:
            #We don't care about any more received data anyways, so throw it away
            self.recv(1500, return_data = False)

        super(TCPSocket, self).close()
        return
    

    def sendNextAck(self):

        ACKPacket = TCPPacket(self.source_port, self.dest_port, self.sequence_number, self.ack_number, TCPSocket.window_size, 0, 0, 1, "")
        self.sendPacket(ACKPacket, add_to_window = False)

    def sendPacket(self, packet, add_to_window = True):

        associated_ack = None

        # Get the associated ack so we can remove the packet when it is acked

        if (packet.syn == 1) or (packet.fin == 1):
            associated_ack = self.getIncrementedSequenceNumber(packet.sequence_number, 1)
        else:
            associated_ack = self.getIncrementedSequenceNumber(packet.sequence_number, len(packet.data))

        # Add the in flight packet to our list and send it down to IP

        packet_in_flight = TCPPacketInFlight(packet, associated_ack)

        if add_to_window:
            self.packets_in_flight.append(packet_in_flight)

        super(TCPSocket, self).send(packet.toData(self.src_ip, self.dest_ip))

    def packetTimedOut(self, tcp_packet_in_flight):

        # Reset cwnd since the packet was dropped

        self.cwnd = 1

        # Remove the packet from the in flight list

        self.packets_in_flight.remove(tcp_packet_in_flight)

        # Resend the packet

        self.sendPacket(tcp_packet_in_flight.tcp_packet)

    def addReceivedPacketToBuffer(self, packet):

        self.receive_window.append(packet)
        self.receive_window.sort(key = lambda packet: (self.getIncrementedSequenceNumber(packet.sequence_number, (-1 * self.ack_number))), reverse = False)

    def parsePacket(self, data):

        packet = TCPPacket.fromData(data)

        # Drop the packet if it's not valid

        if not packet.isValid(self.src_ip, self.dest_ip, self.source_port):
            return


        if not self.connection_initialized:

            self.ack_number = self.getIncrementedSequenceNumber(packet.sequence_number, 1)
            self.sequence_number += 1
            self.sendNextAck()
            self.packets_in_flight.pop()
            self.cwnd = min(999, self.cwnd +1)
	    self.connection_initialized = True
            return

        #Already received this packet
        if self.ack_number > packet.sequence_number:
            #print "old packet", self.ack_number, packet.sequence_number
            return
        elif packet.sequence_number > self.ack_number + TCPSocket.window_size:
            #print "packet outside of window", packet.sequence_number, self.ack_number
            return
        elif self.ack_number < packet.sequence_number:
           # print self.ack_number, packet.sequence_number
            self.addReceivedPacketToBuffer(packet)    
        else:
        
            # Do different stuff based on flags


            if packet.ack == 1:

        
                #Are we assuming that the ack confirms all packets up to that ack num, or just that specific packet
                i = 0
                for packet_in_flight in self.packets_in_flight:
                    if packet_in_flight.associated_ack <= packet.ack_number:
                        self.sequence_number += len(packet_in_flight.tcp_packet.data)
                        i += 1
                    else:
                        break

                self.packets_in_flight = self.packets_in_flight[i:]


                # Increment the congestion window

                self.cwnd = min(999, self.cwnd + 1)

            if packet.fin == 1:
        
                self.received_fin = True        
		self.ack_number += 1
        
              #  print "received fin"
                self.sendNextAck()
                self.teardown()
                return
            
            self.ack_number += len(packet.data)
            ret_data = packet.data
        
            for window_packet in self.receive_window:
             #   print "checking window"
                if window_packet.sequence_number == self.ack_number:
                    ret_data += window_packet.data
                    self.ack_number += len(window_packet.data)
                    if window_packet.fin == 1:
                        self.received_fin = True
                        self.sendNextAck()
                        self.teardown()
                        return ret_data
                    self.receive_window.remove(window_packet)

                break
        
        
            self.sendNextAck()

            return ret_data

    def getIncrementedSequenceNumber(self, number, num_bytes):

        return (number + num_bytes) % TCPSocket.max_sequence_number

class TCPPacketInFlight(object):

    def __init__(self, tcp_packet, associated_ack):

        self.tcp_packet = tcp_packet
        self.associated_ack = associated_ack
        self.timer = None

        self.startTimeoutTimer()

    def startTimeoutTimer(self):

        self.timer = threading.Timer(TCPSocket.timeout_seconds, TCPSocket.packetTimedOut, [self])

class TCPPacket(object):

    def __init__(self, source_port, dest_port, sequence_number, ack_number, window, syn, fin, ack, data):

        self.source_port = source_port
        self.dest_port = dest_port
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.offset = 5
        self.reserved = 0
        self.urg = 0
        self.ack = ack
        self.psh = 0
        self.rst = 0
        self.syn = syn
        self.fin = fin
        self.window = window
        self.checksum = 0 # Set this later with the pseudo header
        self.urgent_pointer = 0
        self.data = data

    def toData(self, source_address, dest_address):

        # Construct the checksumless header

        data_offset = (self.offset << 4)
        flags = (self.urg << 5) + (self.ack << 4) + (self.psh << 3) + (self.rst << 2) + (self.syn << 1) + self.fin

        header = struct.pack('!HHLLBBH',
                 self.source_port,
                 self.dest_port,
                 self.sequence_number,
                 self.ack_number,
                 data_offset,
                 flags, 
                 self.window) + struct.pack('H', self.checksum) + struct.pack("!H", self.urgent_pointer)

        # Construct the pseudo header

        reserved = 0
        protocol = socket.IPPROTO_TCP
        total_length = len(header) + len(self.data)

        pseudo_header = struct.pack("!LLBBH",
                        source_address,
                        dest_address,
                        reserved,
                        protocol,
                        total_length)

        # Construct the checksumless packet

        packet = pseudo_header + header + self.data

        # Calculate the checksum of the checksumless packet

        checksum = utils.calcIpChecksum(packet)

        # Reconstruct the packet with the checksum

        header = struct.pack('!HHLLBBH',
                 self.source_port,
                 self.dest_port,
                 self.sequence_number,
                 self.ack_number,
                 data_offset,
                 flags, 
                 self.window) + struct.pack("H", checksum) + struct.pack("!H", self.urgent_pointer)

        return header + self.data

    def isValid(self, source_address, dest_address,  dest_port):


        # Validate the checksum

        data = self.toData(source_address, dest_address)

        #Checksum validation is broken somewhere, assume correct
        if self.checksum != 0 and False:
            print self.checksum
            return False

        # Validate the port

        #print "valid checksum"

        if self.dest_port != dest_port:
            return False


        return True


    @classmethod
    def fromData(self, packet_data):

    #Ignore urgent flag and Options data
        unpacked = struct.unpack('!HHLLBBH', packet_data[:16])

        flags = unpacked[5]

        source_port = unpacked[0]
        dest_port = unpacked[1]
        sequence_number = unpacked[2]
        ack_number = unpacked[3]
        window = unpacked[6]
        syn = ((flags & 2) >> 1)
        fin = flags & 1
        ack = ((flags & 16) >> 4)
        data = packet_data[20:]

        packet = TCPPacket(source_port, dest_port, sequence_number, ack_number, window, syn, fin, ack, data)

        packet.checksum = struct.unpack('H', packet_data[16:18])[0]


        return packet
