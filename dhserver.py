from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)
IP_POOL = list()

def dhcp_offer(msg):
	pkt = b''
	pkt += b'\x02'	# Opcode
	pkt += b'\x01'	# Hardware type
	pkt += b'\x06'	# Hardware address length
	pkt += b'\x00'	# Hops
	pkt += msg[4:7]	# XID from client discover
	pkt += b'\x00\x00'	# Seconds
	pkt += b'\x00\x00'	# Flags
	# "No broadcast" is ignored?

	# Client IP address (ciaddr), 4 bytes
	pkt += b'\x00'
	pkt += b'\x00'
	pkt += b'\x00'
	pkt += b'\x00'

	# Your IP address (yiaddr), 4 bytes
	pkt += b'\xc0'
	pkt += b'\xa8'
	pkt += b'\x00'
	pkt += b'\x02'

	# Server IP address (siaddr), 4 bytes
	pkt += b'\x00'
	pkt += b'\x00'
	pkt += b'\x00'
	pkt += b'\x00'

	# Relay IP address (giaddr), 4 bytes
	pkt += b'\x00'
	pkt += b'\x00'
	pkt += b'\x00'
	pkt += b'\x00'

	pkt += msg[28:33]	# Client hardware address

	# Server name (64 bytes)
	for i in range(64):
		pkt += b'\x00'

	# File name (128 bytes)
	for i in range(128):
		pkt += b'\x00'

	return pkt

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

# Recieve a UDP message
print("Waiting for UDP messages...")
msg, addr = s.recvfrom(1024)

# Print the client's MAC Address from the DHCP header
print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
for i in range(29, 34):
	print(":" + format(msg[i], 'x'), end = '')
print()

print(format(msg[4:7], 'x'))

for i, m in enumerate(msg):
	string = "msg[" + str(i) + "] = " + format(msg[i], 'x')
	print(string)

# Send a UDP message (Broadcast)
s.sendto(dhcp_offer(msg), DHCP_CLIENT)
