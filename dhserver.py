from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

IP_POOL = [
	["192.168.0.2", "Free"],
	["192.168.0.3", "Free"],
	["192.168.0.4", "Free"],
	["192.168.0.5", "Free"],
	["192.168.0.6", "Free"],
	["192.168.0.7", "Free"],
	["192.168.0.8", "Free"],
	["192.168.0.9", "Free"],
	["192.168.0.10", "Free"]
]

def find_free_ip():
	global IP_POOL
	for ip in IP_POOL:
		if ip[1] == "Free":
			ip[1] = "Taken"
			return ip[0]
	return -1

def dhcp_pkt(msg, yiaddr, type):
	pkt = b''
	pkt += b'\x02'					# Opcode
	pkt += b'\x01'					# Hardware type
	pkt += b'\x06'					# Hardware address length
	pkt += b'\x00'					# Hops
	pkt += msg[4:8]					# XID from client discover
	pkt += b'\x00\x00'				# Seconds
	pkt += b'\x80\x00'				# Flags
	pkt += b'\x00\x00\x00\x00'		# Client IP address (ciaddr), 4 bytes
	pkt += inet_aton(yiaddr)		# Your IP address (yiaddr), 4 bytes
	pkt += b'\x00\x00\x00\x00'		# Server IP address (siaddr), 4 bytes
	pkt += b'\x00\x00\x00\x00'		# Relay IP address (giaddr), 4 bytes
	pkt += msg[28:34]				# Client hardware address

	# Client hardware address padding
	for i in range(10):
		pkt += b'\x00'

	# Server host name
	for i in range(64):
		pkt += b'\x00'

	# Boot file name
	for i in range(128):
		pkt += b'\x00'

	pkt += b'\x63\x82\x53\x63'	# DHCP magic cookie

	if type == "offer":
		pkt += b'\x35\x01\x02'	# Option: DHCP Message Type (Offer)
	else:
		pkt += b'\x35\x01\x05'	# Option: DHCP Message Type (ACK)

	# Option: DHCP Server Identifier
	for i in range(6):
		pkt += b'\x00'

	pkt += b'\x33\x04\x00\x00\x0e\x10'	# Option: IP Address Lease Time
	pkt += b'\x01\x04\xff\xff\xff\x00'	# Option: Subnet Mask (255.255.255.0 or /24)

	# Option: Router
	for i in range(6):
		pkt += b'\x00'

	# Option: Domain Name Server
	for i in range(10):
		pkt += b'\x00'

	# Option: Domain Name
	for i in range(14):
		pkt += b'\x00'

	pkt += b'\xff'	# Option: End

	# Padding
	for i in range(8):
		pkt += b'\x00'

	return pkt

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

while True:
	# Recieve a UDP message
	print("Waiting for UDP messages...")
	msg, addr = s.recvfrom(1024)

	# Print the client's MAC Address from the DHCP header
	print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
	for i in range(29, 34):
		print(":" + format(msg[i], 'x'), end = '')
	print()

	print("Looking for free IP...")
	free_ip = find_free_ip()
	if free_ip == -1:
		print("No free IPs!")
		continue
	else:
		print("Chose " + free_ip + " to offer to client.")

	print("Sending DCP OFFER of address " + free_ip + "!")
	s.sendto(dhcp_pkt(msg, free_ip, "offer"), DHCP_CLIENT)

	print("Sending DCP ACK for address " + free_ip + "!")
	s.sendto(dhcp_pkt(msg, free_ip, "ack"), DHCP_CLIENT)