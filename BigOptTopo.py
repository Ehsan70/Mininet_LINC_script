#!/usr/bin/python

from opticalUtils import MininetOE, OpticalSwitch, OpticalLink
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI


class BigOptTopo(Topo):
    def build(self):

        # Adding optical switches to the network
        self.opt_ann = [] 
        self.opt = [] 
        for o in range(0, 3):
          self.opt_ann.append({"latitude": 30.6+(o*5), "longitude": -122.3, "optical.regens": 0})
          self.opt.append(self.addSwitch('OPT-00'+str(o), dpid='0000ffffffffff0'+str(o) , annotations=self.opt_ann[o], cls=OpticalSwitch))
   
        print ("Size of opt array is "+str(len(self.opt)))
        # Adding packet switches to the network 
        self.pkt = [] 
        for p in range(0,6):
          self.pkt.append(self.addSwitch('pkt-00'+str(p), dpid='000000000000000'+str(p), annotations={"latitude": 53.6, "longitude": -102.3-(5*p)}))
        print ("Size of opt array is "+str(len(self.pkt)))

        # Connecting two optical switches
        try:
          self.makeOptLink(0,1)
          self.makeOptLink(1,2)
        except Exception, e:
          print("Problem occured in making optical links")
        
        # Connecting pkt switches to optical ones
        self.makePktOptLink(0,0)
        self.makePktOptLink(0,1)
        self.makePktOptLink(2,1)
        self.makePktOptLink(3,2)
        self.makePktOptLink(4,2)
        self.makePktOptLink(5,2)

        # Adding hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        # Adding host links
        self.addLink(self.pkt[0], h1, port1=1)
        self.addLink(self.pkt[1], h2, port1=1)
        self.addLink(self.pkt[2], h3, port1=1)
        self.addLink(self.pkt[3], h4, port1=1)
        self.addLink(self.pkt[4], h5, port1=1)
        self.addLink(self.pkt[5], h6, port1=1)

    """
    Make sure p is a packet switch and o is optical switch 
    """
    def makePktOptLink(self,p,o):
      if p < 0 or p > len(self.pkt) :
        raise VallueError(" The p argument must be above 0 and smaller that size of pkt[] which is {1}. Debug: p = {0}".format(p,len(self.pkt)))
      if o < 0 or o > len(self.opt) :  
        raise ValueError(" The o argument must be above 0 and smaller that size of opt[] which is {1}. Debug: o = {0}".format(o, len(self.opt)))
      self.addLink(self.pkt[p], self.opt[o], port1=self.mergeInt(p,o*10), port2=self.mergeInt(o,p*10),
        annotations={"bandwidth": 100000,
          "optical.type": "cross-connect",
          "durable": "true"},
        cls=OpticalLink)


    def makeOptLink(self, a , b):
      if a < 0 or a > len(self.opt) or b < 1 or b > len(self.opt):
        raise ValueError(" Both arguments must be above 0 and smaller that size of opt[].  Debug: p={0}  o={1} ".format(p,o))
      self.addLink(self.opt[a], self.opt[b], port1=self.mergeInt(a,b), port2=self.mergeInt(b,a), 
            annotations={"optical.waves": 80, "optical.type": "WDM", "optical.kms": 1000, "durable": "true"},
            cls=OpticalLink)

    """
    concarenates two integers 
    """
    def mergeInt (self,x,y):
      return int(str(x)+str(y))



if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        controllers = sys.argv[1:]
    else:
        print 'Usage: ./opticalUtils.py (<Controller IP>)+'
        print 'Using localhost...\n'
        controllers = ['127.0.1.1']

    setLogLevel('info')
    net = MininetOE(topo=BigOptTopo(), controller=None,
                    autoSetMacs=True)
    net.addControllers(controllers)
    net.start()
    CLI(net)
    net.stop() 