import sys, os
import struct

#Need to keep track of state for the Identification field and fragment offset

'''
Header is of the form
 0                   1                   2                   3  
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

class IPHeader:

    def __init__(self, source_address, dest_address):

        self.ihl = 5
        self.type_of_service = 0
        self.total_length = 0
        self.id = 0
        self.fragmentation_offset = 0
        self.ttl = 255
        self.protocol = socket.IPPROTO_TCP
        self.checksum = 
        self.source_address = source_address
        self.dest_address = dest_address

    def __init__(self, data):

        unpacked = unpack('!BBHHHBBH4s4s' , self.ihl, self.type_of_service, self.total_length, self.id, self.fragmentation_offset, self.ttl, self.protocol, self.checksum, self.source_address, self.dest_address)
        self.ihl = unpacked[0]
        self.type_of_service = unpacked[1]
        self.total_length = unpacked[2]
        self.id = unpacked[3]
        self.fragmentation_offset = unpacked[4]
        self.ttl = unpacked[5]
        self.protocol = unpacked[6]
        self.checksum = unpacked[7]
        self.source_address = unpacked[8]
        self.dest_address = unpacked[9]

    def to_data():
        return pack('!BBHHHBBH4s4s' , self.ihl, self.type_of_service, self.total_length, self.id, self.fragmentation_offset, self.ttl, self.protocol, self.checksum, self.source_address, self.dest_address)

def calcIpChecksum(header):
    checksum = 0
    
    shorts = struct.unpack('HHHHHHHHHH', header)

    for short in shorts:
	checksum += short
	if checksum & 0x10000:
	    checksum &= 0xFFFF
	    checksum += 1

    return (~checksum) & 0xFFFF

#Header always 20 Bytes as no options are used
#Assuming len(data) <= 1480
def makeIpHeader(source_ip, dest_ip, data):
    Version = 0b0100 #ipv4
    IHL = 0b0101 #size of header in 4byte words
    Type = 0x00
    TotalLen = len(data) + 20
    ID = 0
    Flags = 0b000
    FragmentOffset = 0
    TTL = 0x40
    Protocol = 0x06
    SourceAddr = source_ip
    DestAddr = dest_ip    

    #fmt = (network order) byte, byte, short
    header1 = struct.pack("!BBH", (Version << 4) + IHL, Type, TotalLen) 
    header1 += struct.pack("!HH", ID, Flags << 13 + FragmentOffset)
    header1 += struct.pack("!BB", TTL, Protocol)
    header2 = struct.pack("!LL", SourceAddr, DestAddr)

    Checksum = struct.pack("!H", calcIpChecksum(header1 + '\x00\x00' +  header2))

    header = header1 + Checksum + header2

    return header

def makeIpPacket(source_ip, dest_ip, data):
    header = makeIpHeader(source_ip, dest_ip, data)
    packet = header + data

    return packet


def extractIpHeader(data):
    return data[:20]

def extractIpData(data):
    return data[20:]

