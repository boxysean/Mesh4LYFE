#!/bin/ash

for i in `./ips.sh`; do
	ssh $i cd /root && ./launch.sh
done
