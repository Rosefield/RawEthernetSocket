import sys, os, struct, random, threading
from ip import *

class TCP(object):

    timeout_seconds = 60
    max_packet_size = 1024
    max_sequence_number = 4294967295
    window_size = 65535

    def __init__(self, source_port, dest_port):

        self.source_port = source_port
        self.dest_port = dest_port

        # TCP Stuff

        self.cwnd = 1

        self.sequence_number = random.randint(0, TCP.max_sequence_number)
        self.ack_number = 0

        self.packets_in_flight = []

        # Buffers

        send_buffer = ""
        self.send_buffer_sent_position = 0

    def sendHTTPRequest(self, http_request):

        self.send_buffer = http_request

        self.initiateHandshake()

    def initiateHandshake(self):
        
        SYNPacket = TCPPacket(self.source_port, self.dest_port, self.sequence_number, self.ack_number, TCP.window_size, 1, 0, 0, "")
        
        self.sequence_number = getIncrementedSequenceNumber(self.sequence_number, 1)

        self.sendPacket(SYNPacket)

    def sendPacket(self, packet):

        associated_ack = None

        # Get the associated ack so we can remove the packet when it is acked

        if (packet.syn == 1) or (packet.fin == 1):
            associated_ack = getIncrementedSequenceNumber(packet.sequence_number, 1)
        else:
            associated_ack = getIncrementedSequenceNumber(packet.sequence_number, len(packet.data))

        # Add the in flight packet to our list and send it down to IP

        packet_in_flight = TCPPacketInFlight(packet, associated_ack)
        self.packets_in_flight.append(packet_in_flight)

        IP.sendTCPPacketData(packet.toData())

    def packetTimedOut(self, tcp_packet_in_flight):

        # Reset cwnd since the packet was dropped

        self.cwnd = 1

        # Remove the packet from the in flight list

        self.packets_in_flight.remove(tcp_packet_in_flight)

        # Resend the packet

        self.sendPacket(tcp_packet_in_flight.tcp_packet)

    def recieveTCPPacketData(self, tcp_packet_data):

        packet = TCPPacket.fromData(tcp_packet_data)

        # Drop the packet if it's not valid

        if not packet.isValid(self.source_port):
            return
  
        # Increment the congestion window since the packet was valid

        self.cwnd = MIN(1000, self.cwnd + 1)

        # If this is an ACK, remove the associated packet from our in flight list

        if packet.ack == 1:
            self.packets_in_flight = [packet_in_flight for packet_in_flight in self.packets_in_flight if packet_in_flight.associated_ack != packet.ack_number]

        # Remove the packet with the sequence number 










    def getIncrementedSequenceNumber(number, num_bytes):

        return (number + num_bytes) % TCP.max_sequence_number

class TCPPacketInFlight(object):

    def __init__(self, tcp_packet, associated_ack):

        self.tcp_packet = tcp_packet
        self.associated_ack = associated_ack
        self.timer = None

        self.startTimeoutTimer()

    def startTimeoutTimer(self):

        self.timer = threading.Timer(TCP.timeout_seconds, TCP.packetTimedOut, [self])

class TCPPacket(object):

    def __init__(self, source_port, dest_port, sequence_number, ack_number, window, syn, fin, ack, data):

        self.source_port = source_port
        self.dest_port = dest_port
        self.sequence_number = 0
        self.ack_number = 0
        self.offset = 5
        self.reserved = 0
        self.urg = 0
        self.ack = ack
        self.psh = 1
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

        header = struct.pack('!HHLLBBHHH',
                 self.source_port,
                 self.dest_port,
                 self.sequence_number,
                 self.ack_number,
                 data_offset,
                 flags, 
                 self.window,
                 self.checksum,
                 self.urgent_pointer)

        # Construct the pseudo header

        reserved = 0
        protocol = socket.IPPROTO_TCP
        total_length = len(header) + len(self.data)

        pseudo_header = struct.pack("!4s4sBBH",
                        source_address,
                        dest_address,
                        reserved,
                        protocol,
                        total_length)

        # Construct the checksumless packet

        packet = pseudo_header + header + self.data

        # Calculate the checksum of the checksumless packet

        checksum = TCPPacket.checksum(packet)

        # Reconstruct the packet with the checksum

        header = struct.pack('!HHLLBBHHH',
                 self.source_port,
                 self.dest_port,
                 self.sequence_number,
                 self.ack_number,
                 data_offset,
                 flags, 
                 self.window,
                 checksum,
                 self.urgent_pointer)

        return header + self.data

    def isValid(self, dest_port):

        # Validate the checksum

        data = self.toData()
        if TCPPacket.checksum(data) != self.checksum:
            return False

        # Validate the port

        if self.dest_port != dest_port:
            return False

        return True

    @classmethod
    def checksum(packet_data):
        s = 0
        n = len(data) % 2
        for i in range(0, len(data) - n, 2):
            s += ord(data[i]) + (ord(data[i + 1]) << 8)
        if n:
            s += ord(data[i + 1])
        while (s >> 16):
            print("s >> 16: ", s >> 16)
            s = (s & 0xFFFF) + (s >> 16)
        print("sum:", s)
        s = ~s & 0xffff
        return s

    @classmethod
    def fromData(packet_data):

        unpacked = struct.unpack('!HHLLBBHHH', packet_data[:20])

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

        packet.checksum = unpacked[7]

        return packet
