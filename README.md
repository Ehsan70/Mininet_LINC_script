# Mininet_LINC_script
Contains script that creates optical and packet topologies using Mininet, iControll and LINC.

# Proper Order of Tutorials #
I recomend to do the tutorials in the following order:
 0. Make sure you can create a pure packet network using Mininet python API. There are some online like: [Mininet Walkthrough](http://mininet.org/walkthrough/) and [Introduction to Mininet](https://github.com/mininet/mininet/wiki/Introduction-to-Mininet)
 1. LINCoe_and_iControl.md
 2. POX_iControl_LINC-OE.md
 3. BigOptPktTopo.md
 4. LambdaSwitching.md


# Files #
#### BigOptTopo.py
This python creates a bigger topology than [SimpleOptTopo.py](https://github.com/Ehsan70/Mininet_LINC_script/blob/master/SimpleOptTopo.py). Note that it uses the [opticalUtils.py](https://github.com/Ehsan70/Mininet_LINC_script/blob/master/opticalUtils.py) library which is written by ONOS project. </br>
I recommend to run the code in ONOS virtual machine. You can find instructions on installation [here](https://wiki.onosproject.org/display/ONOS/Basic+ONOS+Tutorial).

#### BigOptPktTopo.md 
This tutorial sets up LINC-OE simple optical topology controlled by iControl and a packet simple topology controlled by POX. Some flows are addded to provide partiall connectivity within network. </br>   
- The tutorial uses `TapSetup.bash` to create Tap interfaces (See description for `TapSetup.bash` file). 
- The tutorial also uses `ComplexMultiTopo.py` to create the packet network. 
- Do the tutorial on [SDN hub all-in-one VM](http://sdnhub.org/tutorials/sdn-tutorial-vm/).

![Alt text](resources/ComplexMultiTopo.jpg?raw=true  "Big Multi Layer Network with more flows")
#### Install_tcpreply.md
This file contains instructions on installing tCP reply on Ubuntu OS. TCPreply is used in POX_iControl_LINC-OE.md and LINCoe_and_iControl.md tutorials.

#### LINCoe_and_iControl.md
This tutorial contains steps to create a pure optical network with linc-oe switches and controlled by iControll. TCPreply is used to send packets into the tap interfaces. </br>
This code was ran on SDNhub virtuall machine which is provided [here](http://sdnhub.org/tutorials/sdn-tutorial-vm/).
Here is the topology created by this tutorial: 
![Alt text](resources/OpticalTopo.jpg?raw=true  "Pure Optical Topology")

#### LambdaSwitching.md
The tutorial quickly sets up LINC-OE simple optical topology controlled by iControl and a simple packet topology controlled by POX. Then trying to perform Lambda Switching on one of the optical switches. 
- The tutorial uses `TapSetup.bash` to create Tap interfaces (See description for `TapSetup.bash` file). 
- The tutorial also uses `ComplexMultiTopo.py` to create the packet network. 
- Do the tutorial on [SDN hub all-in-one VM](http://sdnhub.org/tutorials/sdn-tutorial-vm/).
Here is the topo:
![Alt text](resources/ComplexMultiTopoWithSwitching.jpg?raw=true  "Multi Layer Network and Lambda Switching")
Note that controllers are not shown in the above image. 
#### POX_iControl_LINC-OE.md
This tutorial sets up LINC-OE based simple optical topology controlled by iControl and a simple packet topology controlled by POX controller. This tutorial uses the python file `SimpleOptTopoScratch.py`. This code was ran on SDNhub virtuall machine which is provided [here](http://sdnhub.org/tutorials/sdn-tutorial-vm/).
Below is the optical and packet network topology: </br>
![Alt text](resources/MultiTopo.jpg?raw=true  "Multi Layer Network")

#### SimpleOptTopo.py 
This python code creates optical and packet network connected through Tap interface.  Note that it uses the [opticalUtils.py](https://github.com/Ehsan70/Mininet_LINC_script/blob/master/opticalUtils.py) library which is written by ONOS project. I recommend to run the code in ONOS virtual machine. You can find instructions on installation [here](https://wiki.onosproject.org/display/ONOS/Basic+ONOS+Tutorial). 
See [this tutorial](https://wiki.onosproject.org/display/ONOS/Packet+Optical+Tutorial) on ONOS webpage for the full tutorial.

#### SimpleOptTopoScratch.py 
This file is used for `POX_iControl_LINC-OE.md` tutorial. It constructs the packet layer of the network and connects it to the tap interfaces. 
- It uses only Mininet Python API. 
- Contains a good example of creating TAP interfaces in Mininet Python API. 

#### TapSetup.bash
This file creates X number of Tap interfaces. Where the script gets a number of tap interfaces (X) from the command line (i.e. args).The script takes two arguments: The first one is the number (int) of tap ionterfaces to be created. The second one (string) can take two values: 'up' or 'down'.
- up : for bringing the tap interface up"
- down : for bringing the tap interface down"

It can be used for big topologies. Below is the example commands to execute the script:  
 - Below creates 'tap1' and 'tap2' and it brings them up. </br>
  ```
  sudo bash TapSetup.bash 2 up
  ``` </br>
 - Below brings 'tap1' and 'tap2' down.</br>
  ```
  sudo bash TapSetup.bash 2 down
  ```
  
#### opticalUtils.py
This file is created by onos project for creating optical networks along with packet ones. Here is the [link](https://github.com/opennetworkinglab/onos/tree/master/tools/test/topos ) to the file. `SimpleOptTopo.py` uses this library to create optical networks. This library creates functions that uses linc-oe and sets up the optical netwpork. 

#### sys-PureOptTop.config 
This is a `sys.cofig` that should be used durring the `LINCoe_and_iControl.md` and `POX_iControl_LINC-OE.md`. However, you don't need to use this the tutorials already have the content embedded in the file. 

#### sys-original.config  
This is the sample `sys.config` file which contains comments on how to use the configuration. This file comes with LINC. The original file in LINC_switch can be found [here](https://github.com/FlowForwarding/LINC-Switch/blob/master/rel/files/sys.config.orig). 

#### sys.config 
 TODO
#Setup#
1. Install the virtual machine provided at ONOS website. The VM has multiple users which you can log into. Each used has an environment set up for specific tutorial 
ONOS VM: https://wiki.onosproject.org/display/ONOS/Basic+ONOS+Tutorial 

2. Start the VM and log in with username `optical` and password `optical`
  >>> This section is not done.
