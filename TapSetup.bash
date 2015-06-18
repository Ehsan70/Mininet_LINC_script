#!/bin/bash


# This script creates X number of Tap interfaces. Where the script gets a number of tap interfaces (X) from the command 
# line (i.e. args).
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color



if [ $1 = "help" ] || [ $1 = "--help" ] || [ $1 = "--h" ] || [ $1 = "-h" ] || [ $1 = "-H" ]
then 
echo "[GOAL]This script will create tap interfaces."
echo "[HELP]  The script takes two arguments:" 
echo -e "\tThe first one is the number (int) of tap ionterfaces to be created."
echo -e "\tThe second one (string) can take two values: 'up' or 'down' "
echo -e "\t\tup : for bringing the tap interface up"
echo -e "\t\tdown : for bringing the tap interface down"
echo ""
echo -e "[EXAMPLE] sudo bash TapSetup.bash 2 up"
echo -e "\tAbove creates 'tap1' and 'tap2' and it brings them up"
echo -e "[EXAMPLE] sudo bash TapSetup.bash 2 down"
echo -e "\tAbove brings 'tap1' and 'tap2' down"

else 
	echo "This script will create $1 tap interfaces."
	echo "The first tap is 'tap1' and the last one is named 'tap$1'."
	if [ $2 == "down" ]
	then
		for count in $(seq 1 $1);
		do 
			echo -e "[BASH] ${GREEN}Bringing the tap interface 'tap$count' $2. ${NC}"
			echo -e "\t $(sudo ip link set dev tap$count $2)"
		done 
	else 
		for count in $(seq 1 $1);
		do 
			echo ""
			echo -e "[BASH] ${GREEN}Creating the $count tap interface -> 'tap$count'${NC}"
			echo -e "\t $(sudo tunctl -t tap$count)"
			echo -e "[BASH] ${GREEN}Bringing the tap interface 'tap$count' $2. ${NC}"
			echo -e "\t $(sudo ip link set dev tap$count $2)"
		done 
	fi
fi
