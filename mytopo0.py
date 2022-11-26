"""
Custom Topology:

    +--------+   +--------+
    | client |---| server |
    +--------+   +--------+

"""

from mininet.topo import Topo

class MyTopo(Topo):
	def build(self):
		client = self.addHost('client', ip = None)
		server = self.addHost('server', ip = None)

		self.addLink(client, server)

topos = {'mytopo': (lambda: MyTopo())}
