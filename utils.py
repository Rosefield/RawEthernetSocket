def calcIpChecksum(data):
    checksum = 0
    
    n = len(data) % 2

    for i in range(0, len(data) - n, 2):
	checksum += ord(data[i]) + (ord(data[i+1]) << 8)
    
    if n:
	checksum += ord(data[i])

    while(checksum >> 16):
	checksum = (checksum & 0xffff) + (checksum >> 16)
    
    return (~checksum) & 0xFFFF
