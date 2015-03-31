import sys, os
import struct

# Questions
# Doesn't the kernel handle IP checksums?

class IP(object):

    def sendData(data):
        # Send it
        # TODO: Is the remote IP correct? 
        # TODO: Is the checksum correct? 
        # TODO: Does the protocol identifier match the contents of the encapsulated header?
        # TODO: Handle timeout

class IPPacket(object):

    def __init__(self, source, destination, data):

        self.version = 4
        self.ihl = 5
        self.tos = 0
        self.total_length = 0 # Will be filled by kernel
        self.id = 54321
        self.flags = 0
        self.offset = 0
        self.ttl = 255
        self.protocol = socket.IPPROTO_TCP
        self.checksum = 0 # Will be filled by kernel
        self.source = socket.inet_aton(source)
        self.destination = socket.inet_aton(destination)
        self.data = data

    def toData(self):

        version_ihl = (self.version << 4) + self.ihl
        flags_offset = (self.flags << 13) + self.offset

        ip_header = struct.pack("!BBHHHBBH4s4s",
                    version_ihl,
                    self.tos,
                    self.tl,
                    self.id,
                    flags_offset,
                    self.ttl,
                    self.protocol,
                    self.checksum,
                    self.source,
                    self.destination)

        return ip_header + self.data

    @classmethod
    def getData(packet_data):
        return data[20:]
