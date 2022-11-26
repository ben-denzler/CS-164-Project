"""
Custom Topology:

                           +----------+             
                           |          |             
                           |  server  |
                           |          |
                           +----------+
                                 |
                                 |
                           +-----------+             
                           |           |             
               ____________|  switch0  |____________
              |            |           |           |
              |            +-----------+           |
              |              |      |              |
              |              |      |              |
    +-----------+  +-----------+  +-----------+  +-----------+
    |           |  |           |  |           |  |           |
    |  client0  |  |  client1  |  |  client2  |  |  client3  |
    |           |  |           |  |           |  |           |
    +-----------+  +-----------+  +-----------+  +-----------+

"""

from mininet.topo import Topo

class MyTopo(Topo):
	def build(self):
		client = []
		for i in range(0, 4):
			client.append(self.addHost('client' + str(i), ip = None))
		server = self.addHost('server', ip = None)

		switch = self.addSwitch("switch0")

		for i in range(0, 4):
			self.addLink(client[i], switch)
		self.addLink(server, switch)

topos = {'mytopo': (lambda: MyTopo())}
