from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.link import Link, Intf
from mininet.cli import CLI

class NullIntf( Intf ):
    "A dummy interface with a blank name that doesn't do any configuration"
    def __init__( self, name, **params ):
        self.name = ''

class NullLink( Link ):
    "A dummy link that doesn't touch either interface"
    def makeIntfPair( cls, intf1, intf2, *args, **kwargs ):
        pass
    def delete( self ):
        pass

class OpticalTopoScratch(Topo):
    def addIntf( self, switch, intfName ):
        "Add intf intfName to switch"
        self.addLink( switch, switch, cls=NullLink,
                      intfName1=intfName, cls2=NullIntf )
    def __init__(self):

        self.NUM_OF_HOSTS = 7 # number of hosts
        self.NUM_OF_PKT_SW = 7 # number of packet swiches 
        self.NUM_OF_OPT_SW = 4 # number of optical swiches 

        # Initialize topology
        Topo.__init__(self)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')

        # Adding switches
        s1 = self.addSwitch('s1', dpid="0000ffff00000001")
        s2 = self.addSwitch('s2', dpid="0000ffff00000002")
        s3 = self.addSwitch('s3', dpid="0000ffff00000003")
        s4 = self.addSwitch('s4', dpid="0000ffff00000004")
        s5 = self.addSwitch('s5', dpid="0000ffff00000005")
        s6 = self.addSwitch('s6', dpid="0000ffff00000006")
        s7 = self.addSwitch('s7', dpid="0000ffff00000007")

        # Add links from hosts to OVS
        self.addLink(s1, h1)
        self.addLink(s2, h2)
        self.addLink(s3, h3)
        self.addLink(s4, h4)
        self.addLink(s5, h5)
        self.addLink(s6, h6)
        self.addLink(s7, h7)

        # add links from ovs to linc-oe
    	self.addIntf(s1,'tap1')
    	self.addIntf(s2,'tap2')
    	self.addIntf(s3,'tap3')
    	self.addIntf(s4,'tap4')
    	self.addIntf(s5,'tap5')
    	self.addIntf(s6,'tap6')
    	self.addIntf(s7,'tap7')


        # if you use, sudo mn --custom custom/optical.py, then register the topo:
topos = {'optical': ( lambda: OpticalTopoScratch() )}

def run():
    c = RemoteController('c','0.0.0.0',6633)
    net = Mininet( topo=OpticalTopoScratch(),controller=None,autoSetMacs=True)
    net.addController(c)
    net.start()

    #installStaticFlows( net )
    CLI( net )
    net.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()