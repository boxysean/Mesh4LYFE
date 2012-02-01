#!/bin/ash

for i in `./ips.sh`; do
	scp server.py leds.py launch.sh root@$i:~
done
