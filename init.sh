#!/bin/ash

### settings ###

# mesh network ip address
IP=10.0.0.160

# mesh network network interface
INTERFACE=wlan1

# mesh network network interface channel
CHANNEL=36

# launch master script on this node (set to 1)
MASTER=0

### configure interface ###

ifconfig $INTERFACE mtu 1528
iwconfig $INTERFACE mode ad-hoc essid Mesh4LYFE ap 02:12:34:56:78:9A channel $CHANNEL
batctl if add $INTERFACE
sleep 1
ifconfig bat0 $IP
sleep 1

### launch Mesh4LYFE server ###
. /root/launch.sh
sleep 1

### launch master server (if enabled) ### 
if [[ $MASTER -eq 1 ]]; then
	. /root/launchMaster.sh &
fi

