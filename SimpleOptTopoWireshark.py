#!/usr/bin/python

from opticalUtils import MininetOE, OpticalSwitch, OpticalLink
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI

class SmallOptTopo (Topo):

	def build(self):
		o1ann = { "latitude": 37.6, "longitude": -122.3, "optical.regens": 0 }
		o1 = self.addSwitch('OPT-001', dpid='0000ffffffffff01', 			annotations=o1ann, cls=OpticalSwitch )

		o2ann = { "latitude": 57.6, "longitude": -102.3, 		"optical.regens": 0 }
		o2 = self.addSwitch('OPT-002', dpid='0000ffffffffff02', annotations=o2ann, cls=OpticalSwitch )
        
        o3ann = { "latitude": 67.6, "longitude": -152.3,        "optical.regens": 0 }
        o3 = self.addSwitch('OPT-003', dpid='0000ffffffffff03', annotations=o3ann, cls=OpticalSwitch )
        


		pkt1 = self.addSwitch( 'PK1-R10', dpid='0000000000000001', 	annotations={"latitude": 37.6, "longitude": -122.3} )
		pkt2 = self.addSwitch('PK2-R10', dpid='0000000000000002',  	annotations={ "latitude": 33.9, "longitude": -118.4 } )
        
        #Connecting two optical switches
		self.addLink( o1, o2, port1=10, port2=20,annotations={ "optical.waves":80, "optical.type":"WDM", "optical.kms":1000, "durable":"true" }, cls=OpticalLink )

        # Connecting pkt2 to O2 	
		self.addLink(pkt2,o2, port1=22, port2=21, 
        	annotations={ "bandwidth": 100000, 
        	"optical.type": "cross-connect", 
        	"durable": "true" }, 
        	cls=OpticalLink )

        # Connecting pkt1 to O1 	
		self.addLink(pkt1,o1, port1=12, port2=11, 
        	annotations={ "bandwidth": 100000, 
        	"optical.type": "cross-connect", 
        	"durable": "true" }, 
        	cls=OpticalLink )

        # Adding hosts
		h1 = self.addHost( 'h1' )
		h2 = self.addHost( 'h2' )

		self.addLink( pkt1, h1, port1=1 )
		self.addLink( pkt2, h2, port1=1 )

if __name__ == '__main__':
    import sys
    if len( sys.argv ) >= 2:
        controllers = sys.argv[1:]
    else:
        print 'Usage: ./opticalUtils.py (<Controller IP>)+'
        print 'Using localhost...\n'
        controllers = [ '127.0.1.1' ]

    setLogLevel( 'info' )
    net = MininetOE( topo=SmallOptTopo(), controller=None, 
    	autoSetMacs=True )
    net.addControllers(controllers)
    input("Press Enter to continue ...")
    net.start()
    CLI( net )
    net.stop()