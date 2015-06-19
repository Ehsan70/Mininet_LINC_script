<b>Goal</b>: First quickly setting up LINC-OE simple optical topology controlled by iControl and a packet simple topology controlled by POX. Then trying to perform Lambda Switching on one of the optical switches. </br>

<b>Requirements:</b>
A basic knowlege of LINC-OE, TAP interfaces, POX, Erlang language , Lambda Switchin and linux CLI is required. 
Doing [this tutorial](https://github.com/Ehsan70/Mininet_LINC_script/blob/master/POX_iControl_LINC-OE.md) and [this](https://github.com/Ehsan70/Mininet_LINC_script/blob/master/BigOptPktTopo.md) is a must. 

<b>Environment: </b> I have used the VM from sdn hub, I recommond you do the same. Link for installation is provided below: http://sdnhub.org/tutorials/sdn-tutorial-vm/

<b>Road Map: </b>This document has two sections for setup: 

 1. setting up the optical and packet network </br>
 2. performing Lambda switching


# 1. setting up the optical and packet network 

### setting up the optical network ###
 a. Run iControl: 
 ```shell
 > cd loom/iControl
 > rel/icontrol/bin/icontrol console
 ```
 The iControl starts and listens on 0.0.0.0:6653 </br>
 b. Clearting the tap interfaces: </br>
 For this section I have created a bash script that takes care of tap interfaces. 
 ```shell
 sudo bash TapSetup.bash 7 up
 ```
 The first argument is the number of tap interfaces and the second one is `up` which also brings the interfaces up. 
 c. Set up the `sys.config` file: 
 `rel/files/sys.config` file for the network shown above should looks as following:
 ```erlang
[{linc,
  [{of_config,disabled},
   {capable_switch_ports,
    [{port,1,[{interface,"tap1"}]},
     {port,2,[{interface,"tap2"}]},
     {port,3,[{interface,"tap3"}]},
     {port,4,[{interface,"dummy"}, {type, optical}]},
     {port,5,[{interface,"dummy"}, {type, optical}]},
     {port,6,[{interface,"tap4"}]},
     {port,7,[{interface,"dummy"}, {type, optical}]},
     {port,8,[{interface,"dummy"}, {type, optical}]},
     {port,9,[{interface,"dummy"}, {type, optical}]},
     {port,10,[{interface,"tap6"}]},
     {port,11,[{interface,"tap7"}]},
     {port,12,[{interface,"dummy"}, {type, optical}]},
     {port,13,[{interface,"tap5"}]}
    ]},
   {capable_switch_queues, []},
   {optical_links, [{{1,4}, {2,1}}, {{2,3},{3,1}}]},
   {logical_switches,
    [{switch,1,
      [{backend,linc_us4_oe},
       {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
       {controllers_listener,disabled},
       {queues_status,disabled},
       {datapath_id, "00:00:00:00:00:01:00:01"},
       {ports,[{port,1,[{queues,[]}, {port_no, 1}]},
       		   {port,2,[{queues,[]}, {port_no, 2}]},
       		   {port,3,[{queues,[]}, {port_no, 3}]},
               {port,4,[{queues,[]}, {port_no, 4}]}
              ]}]},
     {switch,2,
      [{backend,linc_us4_oe},
       {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
       {controllers_listener,disabled},
       {queues_status,disabled},
       {datapath_id, "00:00:00:00:00:01:00:02"},
       {ports,[{port,5,[{queues,[]}, {port_no, 1}]},
       		   {port,6,[{queues,[]}, {port_no, 2}]},
       		   {port,7,[{queues,[]}, {port_no, 3}]},
               {port,8,[{queues,[]}, {port_no, 4}]}
              ]}]},
     {switch,3,
      [{backend,linc_us4_oe},
       {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
       {controllers_listener,disabled},
       {queues_status,disabled},
       {datapath_id, "00:00:00:00:00:01:00:03"},
       {ports,[{port,9,[{queues,[]}, {port_no, 1}]},
               {port,10,[{queues,[]}, {port_no, 2}]},
               {port,11,[{queues,[]}, {port_no, 3}]}
              ]}]},
     {switch,4,
      [{backend,linc_us4_oe},
       {controllers,[{"Switch0-Controller","localhost",6653,tcp}]},
       {controllers_listener,disabled},
       {queues_status,disabled},
       {datapath_id, "00:00:00:00:00:01:00:04"},
       {ports,[{port,12,[{queues,[]}, {port_no, 1}]},
               {port,13,[{queues,[]}, {port_no, 2}]}
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

### setting up the packet network ###
 a. Run POX 
  ```shell
  > ./pox.py log.level --debug forwarding.tutorial_l2_hub
  ```
  This will instanciate a hub controller. So here is what is happening nder the hood: a packet comes on one port of the packet switch, the switch doesn't know what to do so it asks the pox controller. The pox will tell the switch to broadcast the packet (meaning send it to all ports; acts like a hub). This would send the packet on to the port which is connected to the tap interface. 
  The pox will start up and listens on 0.0.0.0:6633  </br></br>
 b. Move to the directory where this repository is cloned into, and tun python topo using python API. 
  ```shell
  > sudo -E python ComplexMultiTopo.py
  ```
  The `ComplexMultiTopo.py` file will create a packet topolgy which includes two switches and two host. 
  The switches are connected to hosts on one end and on the other end they are connected to tap interfaces. 
  Note that tap interfaces are connected linc-oe switches.  
 
 Here is the topolgu of what we have right now:
 ![Alt text](resources/ComplexMultiTopo.jpg?raw=true  "Multi Layer Network")
#  2. performing Lambda switching
Now the optical and packet network are ready and connected. 
If you run `pingall` on mininet CLI, all of the packets should be droped. 
```
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X X X X X 
h2 -> X X X X X X 
h3 -> X X X X X X 
h4 -> X X X X X X 
h5 -> X X X X X X 
h6 -> X X X X X X 
h7 -> X X X X X X 
*** Results: 100% dropped (0/42 received)
```
Of course you can have wireshark probing any of the interfaces.</br>
Before we add flows we need to check what the switch key is for each optical switch. That can be done using 
```erlang
iControl> iof:switches(). 
```
The bove with return something like: 
```
(icontrol@127.0.0.1)1> iof:switches().
Switch-Key DatapathId                       IpAddr            Version
---------- -------------------------------- ----------------- -------
*1         00:00:00:00:00:01:00:04          {127,0,0,1}       4      
 2         00:00:00:00:00:01:00:02          {127,0,0,1}       4      
 3         00:00:00:00:00:01:00:03          {127,0,0,1}       4      
 4         00:00:00:00:00:01:00:01          {127,0,0,1}       4      
ok

```
The first line means: the switch with Datapath ID (DPID) of 00:00:00:00:00:01:00:04 has the switch key value of 1. The second and third can be observed similarly. </br>
> Note that the follwoing code may need to be changed based on switch keys. 

Now, let's add some flows: 
<b> Connecting h1 to h7 -> purpple channel <b></br>
```erlang
 iControl> iof:oe_flow_tw(4,100,1,4,20).
 iControl> iof:oe_flow_ww(2,100,1,20,3,20).
 iControl> iof:oe_flow_wt(3,100,1,20,3).
 
 iControl> iof:oe_flow_wt(4,100,4,20,1).  
 iControl> iof:oe_flow_ww(2,100,3,20,1,20). 
 iControl> iof:oe_flow_tw(3,100,3,1,20). 
 ```

<b> Connecting h2 to h4 -> Brown channel <b></br>
```erlang
 iControl> iof:oe_flow_tw(4,100,2,4,40).
 iControl> iof:oe_flow_wt(2,100,1,40,2).
 
 iControl> iof:oe_flow_wt(4,100,4,40,2).  
 iControl> iof:oe_flow_tw(2,100,2,1,40). 
```
<c> Connecting h3 to h6 -> Orange/yellow channel <b></br>
```erlang
 iControl> iof:oe_flow_tw(4,100,3,4,30).
 iControl> iof:oe_flow_ww(2,100,1,30,3,30).
 iControl> iof:oe_flow_wt(3,100,1,30,2).

 iControl> iof:oe_flow_wt(4,100,4,30,3).  
 iControl> iof:oe_flow_ww(2,100,3,30,1,30). 
 iControl> iof:oe_flow_tw(3,100,2,1,30). 
 ```  
With the above set of flows, `pingall` should return: 
```
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X X X X h7 
h2 -> X X h4 X X X 
h3 -> X X X X h6 X 
h4 -> X h2 X X X X 
h5 -> X X X X X X 
h6 -> X X h3 X X X 
h7 -> h1 X X X X X 
*** Results: 85% dropped (6/42 received)
```
How about green channel? It uses the same channel as oragne channel. Both have channel 30. 

```erlang
 iControl> iof:oe_flow_tw(4,100,3,4,10).
 iControl> iof:oe_flow_ww(2,100,1,10,4,30).
 iControl> iof:oe_flow_wt(1,100,1,30,2).

 iControl> iof:oe_flow_wt(4,100,4,10,3).  
 iControl> iof:oe_flow_ww(2,100,4,30,1,10). 
 iControl> iof:oe_flow_tw(1,100,2,1,30). 
```





