from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

IP_POOL = [
	("192.168.0.2", "Free"),
	("192.168.0.3", "Free"),
	("192.168.0.4", "Free"),
	("192.168.0.5", "Free"),
	("192.168.0.6", "Free"),
]

def find_free_ip():
	for ip in IP_POOL:
		print("Looking at " + ip[0] + " which is " + ip[1])
		if ip[1] == "Free":
			ip[1] == "Taken"
			print("Returning " + ip[0] + " which is " + ip[1])
			return ip[0]

# def ip_as_hex(ip):
# 	hex_ip = b''
# 	octets = ip.split('.')

# 	hex_ip += bytes(hex(int(octets[0])), 'utf-8')
# 	print("bytes(hex(int(octets[0])) = " + format(bytes(hex(int(octets[0])), 'utf-8')))
# 	print("hex_ip[0] = " + format(hex_ip[0], 'x'))

# 	hex_ip += bytes(hex(int(octets[1])), 'utf-8')
# 	hex_ip += bytes(hex(int(octets[2])), 'utf-8')
# 	hex_ip += bytes(hex(int(octets[3])), 'utf-8')

# 	print("IP address in hex: ")
# 	for i in range(0, 3):
# 		print(format(hex_ip[i], 'x') + ' ', end = '')
# 	print()

# 	return hex_ip

def dhcp_offer(msg, yiaddr):
	pkt = b''
	pkt += b'\x02'					# Opcode
	pkt += b'\x01'					# Hardware type
	pkt += b'\x06'					# Hardware address length
	pkt += b'\x00'					# Hops
	pkt += msg[4:8]					# XID from client discover
	pkt += b'\x00\x00'				# Seconds
	pkt += b'\x80\x00'				# Flags
	pkt += socket.inet_aton(yiaddr)	# Client IP address (ciaddr), 4 bytes
	pkt += b'\xc0\xa8\x00\x02'		# Your IP address (yiaddr), 4 bytes
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
	pkt += b'\x35\x01\x02'		# Option: DHCP Message Type (Offer)

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

# Recieve a UDP message
print("Waiting for UDP messages...")
msg, addr = s.recvfrom(1024)

# Print the client's MAC Address from the DHCP header
print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
for i in range(29, 34):
	print(":" + format(msg[i], 'x'), end = '')
print()

# for i, m in enumerate(msg):
# 	string = "msg[" + str(i) + "] = " + format(msg[i], 'x')
# 	print(string)

# Send a UDP message (Broadcast)
free_ip = find_free_ip()
s.sendto(dhcp_offer(msg, free_ip), DHCP_CLIENT)
