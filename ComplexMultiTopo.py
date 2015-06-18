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

class ComplexMultiTopo(Topo):
    def addIntf( self, switch, intfName ):
        "Add intf intfName to switch"
        self.addLink( switch, switch, cls=NullLink,
                      intfName1=intfName, cls2=NullIntf )
    def __init__(self):
        
        self.NUM_OF_HOSTS = 15 # number of hosts
        self.NUM_OF_PKT_SW = 7 # number of packet swiches 
        self.NUM_OF_OPT_SW = 4 # number of optical swiches 
        # NOte that optical switches are mcreated in sys.config

        # Initialize topology
        Topo.__init__(self)

        self.hosts = []
        self.pkt_swt = [] 

        # Add hosts 
        for h in range(1,self.NUM_OF_HOSTS+1):
        	pass	
           #self.hosts.append(self.addHost('h'+str(h)))

        # Add switches
        for p in range(1,self.NUM_OF_PKT_SW+1) :
        	pass
            #self.pkt_swt.append(self.addSwitch('p'+str(p), dpid="0000ffff000000%02d"%p))
        
        # Add links from hosts to OVS
        for i, p_sw in enumerate(self.pkt_swt,start=1):
        	self.addLink(p_sw, h[2*i-1])
        	self.addLink(p_sw, h[2*i])

        # add links from ovs to linc-oe			
        for i, p_sw in enumerate(self.pkt_swt,start=1) :
        	self.addIntf(p_sw,'tap'+str(i))



        # if you use, sudo mn --custom custom/optical.py, then register the topo:
topos = {'optical': ( lambda: ComplexMultiTopo() )}

def run():
    c = RemoteController('c','0.0.0.0',6633)
    net = Mininet( topo=ComplexMultiTopo(),controller=None,autoSetMacs=True)
    net.addController(c)
    net.start()

    #installStaticFlows( net )
    CLI( net )
    net.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()