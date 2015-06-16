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

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        s1 = self.addSwitch('s1', dpid="0000ffff00000001")
        s2 = self.addSwitch('s2', dpid="0000ffff00000002")

        # Add links from hosts to OVS
        self.addLink(s1, h1)
        self.addLink(s2, h2)


        # add links from ovs to linc-oe
        # sorry about the syntax :(
        self.addIntf(s1,'tap0')
        self.addIntf(s2,'tap1')


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

