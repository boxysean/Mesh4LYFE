#!/bin/ash

for i in `./ips.sh`; do
	ping -c 1 $i
done

