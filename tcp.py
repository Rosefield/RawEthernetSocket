import sys, os, struct

class TCP(object):

    def __init__(self):

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

        checksum = checksum(packet)

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

    @classmethod
    def getData(packet_data):
        return packet_data[20:]
