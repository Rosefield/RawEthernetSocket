OVERVIEW:

For this project, we decided to use Python for its native raw socket support. We created classes for TCP, IP, and Ethernet sockets, inheriting from each other in that order. We also created classes for each type of packet. These classes were able to be initialized with raw data and included methods which converted them to raw data. This parsing was useful for reading and setting properties without having to do manual bit manipulation every time. 

To start, we created the HTTP file which includes utilities to build HTTP GET requests. This also includes the ability to validate, parse, and save the data from the response body with the correct filename. These methods are used in our rawhttpget.py file at the top of our stack. These requests are then passed from TCP to IP to Ethernet, wrapping the data in the respective header and passing it along the chain.

TCP was one of the biggest challenges because of its complexity. Since data is expected to be retuned in order, we had to keep track of a lot of state. We created explicit functions to deal with the handshake and teardown as well as a parsePacket function that manages the heavy lifting of deconstructing the packets and performing the correct action such as sending ACKs or increasing the congestion window upon each successful packet sent. In addition to our buffers, we also keep track of our in-flight packets using the TCPPacketInFlight class which includes a timer that manages timeouts and resends the packet if necessary.

For checksums, we created a utility function that took a generic packet and returned its checksum. One problem we faced was getting a correct checksum for TCP packets before we found out about the required pseudo-header.

At the ethernet layer we construct the frame header and pad the data to the minimum ethernet frame size. Additionally, the ethernet layer takes care of getting the gateway's IP address from the system, then crafting an arp request (and waiting for a response) to get the MAC address of the gateway so that packets can be sent to the rest of the internet. Overall, the ethernet layer was pretty simple without too many gotchas.

WORK DELEGATION:

Work was done both independently and utilizing peer programming. Gavin did HTTP and Schuyler handled Ethernet. TCP and IP were done collaboratively.

RUNNING:

- First run "iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP"
- execute "sudo ./rawhttpget [URL]" to download the file
