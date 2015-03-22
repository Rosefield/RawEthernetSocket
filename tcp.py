import sys, os, struct



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
