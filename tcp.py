import sys, os, struct

class TCP(object):

    def __init__(self):

    def sendHTTPRequest(tcp_packet_data):

        # Send it
        # TODO: Is the remote IP correct? 
        # TODO: Is the checksum correct? (Is this not handled by the kernel?)
        # TODO: Does the protocol identifier match the contents of the encapsulated header?
        # TODO: Handle timeout

    def recieveTCPPacketData(tcp_packet_data):

        tcp_packet = TCPPacket.fromData(tcp_packet_data)

        if tcp_packet.isValid():
            HTTPPacket.recieveHTTPPacketData(tcp_packet.data)

        # Send it
        # TODO: Is the remote IP correct? 
        # TODO: Is the checksum correct? (Is this not handled by the kernel?)
        # TODO: Does the protocol identifier match the contents of the encapsulated header?
        # TODO: Handle timeout

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

    def isValid():

        return True

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
