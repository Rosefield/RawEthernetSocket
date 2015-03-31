import sys, os
import struct

# Questions
# Doesn't the kernel handle IP checksums?

class IP(object):

    def __init__(self):

    def sendData(data):
        # Send it
        # TODO: Is the remote IP correct? 
        # TODO: Is the checksum correct? (Is this not handled by the kernel?)
        # TODO: Does the protocol identifier match the contents of the encapsulated header?
        # TODO: Handle timeout

class IPPacket(object):

    def __init__(self, source_address, destination_address, data):

        self.version = 4
        self.ihl = 5
        self.tos = 0
        self.total_length = 0 # Will be set by the kernel
        self.id = 54321
        self.flags = 0
        self.offset = 0
        self.ttl = 255
        self.protocol = socket.IPPROTO_TCP
        self.checksum = 0 # Will be set by the kernel
        self.source_address = source_address
        self.destination_address = destination_address
        self.data = data

    def toData(self):

        version_ihl = (self.version << 4) + self.ihl
        flags_offset = (self.flags << 13) + self.offset

        header = struct.pack("!BBHHHBBH4s4s",
                 version_ihl,
                 self.tos,
                 self.total_length,
                 self.id,
                 flags_offset,
                 self.ttl,
                 self.protocol,
                 self.checksum,
                 self.source_address,
                 self.destination_address)

        return header + self.data

    @classmethod
    def fromData(packet_data):

        unpacked = struct.unpack("!BBHHHBBH4s4s", packet_data[:20])

        source_address = unpacked[8]
        destination_address = unpacked[9]
        data = packet_data[20:]

        packet = IPPacket(source_address, destination_address, data)

        packet.checksum = unpacked[7]

        return packet
