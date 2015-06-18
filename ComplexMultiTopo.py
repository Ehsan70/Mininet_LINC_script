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


        o1 = self.addSwitch('o1', dpid="0000ffff00000001")
        o2 = self.addSwitch('o2', dpid="0000ffff00000002")
        o3 = self.addSwitch('o3', dpid="0000ffff00000003")
        o4 = self.addSwitch('o4', dpid="0000ffff00000004")
        o5 = self.addSwitch('o5', dpid="0000ffff00000005")
        o6 = self.addSwitch('o6', dpid="0000ffff00000006")
        o7 = self.addSwitch('o7', dpid="0000ffff00000007")

        # Add links from hosts to OVS
        self.addLink(o1, h1)
        self.addLink(o2, h2)
        self.addLink(o3, h3)
        self.addLink(o4, h4)
        self.addLink(o5, h5)
        self.addLink(o6, h6)
        self.addLink(o7, h7)

        # add links from ovs to linc-oe
        # sorry about the syntax :(
        self.addIntf(o1,'tap1')
        self.addIntf(o2,'tap2')
        self.addIntf(o3,'tap3')
        self.addIntf(o4,'tap4')
        self.addIntf(o5,'tap5')
        self.addIntf(o6,'tap6')
        self.addIntf(o7,'tap7')


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