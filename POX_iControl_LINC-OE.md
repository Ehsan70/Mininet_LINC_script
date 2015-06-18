<b>Goal</b>: Seting up LINC-OE simple optical topology controlled by iControl and a packet simple topology controlled by POX. 
<b>Requirements:</b>
A basic knowlege of LINC-OE, TAP interfaces, POX, Erlang language and linux CLI is required. 
Doing https://github.com/Ehsan70/Mininet_LINC_script/blob/master/LINCoe_and_iControl.md tutorial is a must. 

<b>Environment: </b> I have used the VM from sdn hub, I recommond you do the same. Link for installation is provided below: http://sdnhub.org/tutorials/sdn-tutorial-vm/

<b>Road Map: </b>This document has two sections for setup: 

 1. setting up the optical network   
 2. setting up the packet network </br>

Then the tutorial would run couple of experminets. After the experminet the tutorial talkes about the details of the network and what is goingt on under the hood.   

<b>Notations: </b>
 - `>` means the linuc command line <br>
 - `iControl>` Means the iControll command line
 
> Before we start have a look at the image at the end of this file to get a sense of what the topology will be. 

# 1. setting up the optical network #
 a. Run iControl: 
 ```shell
 > cd loom/iControl
 > rel/icontrol/bin/icontrol console
 ```
 The iControl starts and listens on 0.0.0.0:6653 </br>
 b. Clearting the tap interfaces: 
 ```shell
 > sudo tunctl -t tap0
 > sudo tunctl -t tap1
 > sudo ip link set dev tap0 up
 > sudo ip link set dev tap1 up
 ```
 c. Set up the `sys.config` file: 
 `rel/files/sys.config` file for the network shown above should looks as following:
 ```erlang
 [{linc,
   [{of_config,disabled},
    {capable_switch_ports,
     [{port,1,[{interface,"tap0"}]},
      {port,2,[{interface,"dummy"}, {type, optical}]},
      {port,3,[{interface,"dummy"}, {type, optical}]},
      {port,4,[{interface,"dummy"}, {type, optical}]},
      {port,5,[{interface,"dummy"}, {type, optical}]},
      {port,6,[{interface,"tap1"}]}
     ]},
    {capable_switch_queues, []},
    {optical_links, [{{1,2}, {2,1}}, {{2,2},{3,1}}]},
    {logical_switches,
     [{switch,1,
       [{backend,linc_us4_oe},
        {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
        {controllers_listener,disabled},
        {queues_status,disabled},
        {datapath_id, "00:00:00:00:00:01:00:01"},
        {ports,[{port,1,[{queues,[]}, {port_no, 1}]},
                {port,2,[{queues,[]}, {port_no, 2}]}
               ]}]},
      {switch,2,
       [{backend,linc_us4_oe},
        {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
        {controllers_listener,disabled},
        {queues_status,disabled},
        {datapath_id, "00:00:00:00:00:01:00:02"},
        {ports,[{port,3,[{queues,[]}, {port_no, 1}]},
                {port,4,[{queues,[]}, {port_no, 2}]}
               ]}]},
      {switch,3,
       [{backend,linc_us4_oe},
        {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
        {controllers_listener,disabled},
        {queues_status,disabled},
        {datapath_id, "00:00:00:00:00:01:00:03"},
        {ports,[{port,5,[{queues,[]}, {port_no, 1}]},
                {port,6,[{queues,[]}, {port_no, 2}]}
               ]}]}
     ]}]},
  {of_protocol, [{no_multipart, false}]},
  {enetconf,
   [{capabilities,[{base,{1,1}},{startup,{1,0}},{'writable-running',{1,0}}]},
    {callback_module,linc_ofconfig},
    {sshd_ip,any},
    {sshd_port,1830},
    {sshd_user_passwords,[{"linc","linc"}]}]},
  {epcap,
   [{verbose, false},
    {stats_interval, 10},
    {buffer_size, 73400320}]},
  {lager,
   [{handlers,
     [{lager_console_backend,debug},
      {lager_file_backend,
       [{"log/error.log",error,10485760,"$D0",5},
        {"log/debug.log",debug,10485760,"$D0",5},
        {"log/console.log",info,10485760,"$D0",5}]}]}]},
  {sasl,
   [{sasl_error_logger,{file,"log/sasl-error.log"}},
    {errlog_type,error},
    {error_logger_mf_dir,"log/sasl"},
    {error_logger_mf_maxbytes,1048576000000},
    {error_logger_mf_maxfiles,5}]},
  {sync,
   [{excluded_modules, [procket]}]}].
 ```
 d. start LINC-OE: 
 ```shell
 > make rel && sudo rel/linc/bin/linc console
 ```
 e. Add some flows to the optical switches. 
 Type the following commands in the iControl window:
 ```erlang
 iControl> iof:oe_flow_tw(2,100,1,2,20).
 iControl> iof:oe_flow_ww(1,100,1,20,2,20).
 iControl> iof:oe_flow_wt(3,100,1,20,2).
 
 iControl> iof:oe_flow_wt(2,100,2,20,1).
 iControl> iof:oe_flow_ww(1,100,2,20,1,20).
 iControl> iof:oe_flow_tw(3,100,2,1,20).
 ```
 > Note that you need to add flows for both directions. 
 
 So now if put stuff (packets) in one of the tap interfaces (using tcpreply) it will apear on the tap. 
 
 > Follow the LINCoe_and_iControl.md tutorial to check if you have done all the steps right. 
 


# 2. setting up the packet network #
 a. Run POX 
  ```shell
  > ./pox.py log.level --debug forwarding.tutorial_l2_hub
  ```
  This will instanciate a hub controller. So here is what is happening nder the hood: a packet comes on one port of the packet switch, the switch doesn't know what to do so it asks the pox controller. The pox will tell the switch to broadcast the packet (meaning send it to all ports; acts like a hub). This would send the packet on to the port which is connected to the tap interface. 
  The pox will start up and listens on 0.0.0.0:6633  </br></br>
 b. Move to the directory where this repository is cloned into, and tun python topo using python API. 
  ```shell
  > sudo -E python SimpleOptTopoScratch.py
  ```
  The `SimpleOptTopoScratch.py` file will create a packet topolgy which includes two switches and two host. 
  The switches are connected to hosts on one end and on the other end they are connected to tap interfaces. 
  Note that tap interfaces are connected linc-oe switches.  
 
# Experiment senario #
## Experminet One ##
Now the optical and packet network are ready and connected. 
If you run `pingall` on mininet CLI, none of the packets should be droped. 

Of course you can have wireshark probing Tap0 or Tap1 interfaces.</br>
Let's remove all of the optical flows. To do so, execute the following:
```erlang
iControl> iof:clear_flows(1,0). 
iControl> iof:clear_flows(2,0).
iControl> iof:clear_flows(3,0).
%% The below commands will dump the flows installed on specific switch keys. You could execute them to check the flows. 
iControl> iof:flows(1).
iControl> iof:flows(2).
iControl> iof:flows(3).
```
Now, if you try `pingall` 100 percent of the packets will drop. </br>

## Experiment Two ##

Now lets recreate one direction of the path in the optical network. Note that the ping packets are sent by one of the host but cannot be received. This means, we should expect all packets to be droped. Let's go ahead and do what we talked about: 

Enter the flowwing in the iControll window: 
```erlang
iControl> iof:clear_flows(1,0). 
iControl> iof:clear_flows(2,0).
iControl> iof:clear_flows(3,0).
```
Run `pingall` in mininet CLI window. You will see that all the packets are dropped. 

## Experiment Three ##
<b>Assumption:</b> I assumed you did the last experminet. 
Now, let's create other direction of the path. Enter the following in iControl window: 
```erlang
iControl> iof:oe_flow_wt(2,100,2,20,1).
iControl> iof:oe_flow_ww(1,100,2,20,1,20).
iControl> iof:oe_flow_tw(3,100,2,1,20).
```
Run `pingall` in mininet CLI window. You will see that none of the packets are droped. 
 
# Details of The Network # 
One of the hosts (host A) sends a packet to the other one (host B). A packet reaches the port of the packet switch, the switch doesn't know what to do so it asks the pox controller. The pox controller is instantiated as a hub, so it will tell the switch to broadcast the packet (meaning send it to all ports; acts like a hub). This would send the packet on to the port which is connected to the tap interface. When the packet reaches the TAP interface it has leaved the packet network and has entered the optical network. So now if the optical switches are set up properlly (i.e. the flows are right) then the packets reaches the other tap interfcae. Otherwise, if optical switches don't have the proper flows then the packet is droped/lost. Below is and image of network topologies.      
 
![Alt text](resources/MultiTopo.jpg?raw=true  "Multi Layer Network")
 
 
 
 
 
 
 
 
 
