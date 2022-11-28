from socket import *

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)
IP_POOL = list()	

def DHCP_OFFER(ip_address):
	pkt = b''
	pkt += b'\x02'
	pkt += b'\x01'
	pkt += b'\x06'
	pkt += b'\x00'

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

for i, m in enumerate(msg):
	string = "msg[" + str(i) + "] = " + format(msg[i], 'x')
	print(string)

print(format(msg, 'x'))

# Send a UDP message (Broadcast)
s.sendto(b'192.168.0.2', DHCP_CLIENT)
