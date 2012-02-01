#
# this program is a "master signal" for the Mesh4LYFE nodes by broadcasting
# "update" and "display" messages in lockstep.
#
# restarts the evolution after some number of generations between GEN_MIN
# and GEN_MAX. sends "random" messages to trigger a random state at the start
# of each evolution.
#
# todo: would be cool to add a listener here to detect when the game of life
# is in a stable state, rather than having GEN_MIN and GEN_MAX to restart
# the evolution chain when it may be in full swing
#

import socket
import sys
import time
import random

# bounds of the number of generations per evolution chain; randomly chosen
# between these two numbers
GEN_MIN = 8
GEN_MAX = 28

# server.py port
port = 31337

# time in seconds to pause between messages, i.e., framerate
sleepTime = 0.20

# broadcast IP
broadcastIp = "10.255.255.255"

# list of routers in order (L-R, or possibly R-L, i don't know)
routers = [
	"",
	"10.0.0.165",
	"10.0.0.180",
	"10.0.0.115",
	"10.0.0.160",
	"10.0.0.155",
	"10.0.0.175",
	"10.0.0.150",
	"10.0.0.110",
	""
]
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def send(s, ip, cmd):
	s.sendto(cmd, (ip, port))

time.sleep(10)

print "set neighbours"

for i in range(1,len(routers)-1):
	if len(routers[i-1]):
		send(s, routers[i], "neighbour 0 %s" % routers[i-1])
		print "L", routers[i-1]
		
	print "C", routers[i]
	
	if len(routers[i+1]):
		send(s, routers[i], "neighbour 1 %s" % routers[i+1])
		print "R", routers[i+1]
		
	print ""
	
rounds = 0

while 1:
	if rounds <= 0:
		print "on"
		send(s, broadcastIp, "on")
		time.sleep(sleepTime)
		
		print "off"
		send(s, broadcastIp, "off")
		time.sleep(2*sleepTime)
		
		print "random"
		rounds = random.randint(GEN_MIN, GEN_MAX)
		send(s, broadcastIp, "random")
		time.sleep(sleepTime/2)

	print "broadcast"
	send(s, broadcastIp, "broadcast")
	time.sleep(sleepTime)

	print "display"
	send(s, broadcastIp, "display")
	time.sleep(sleepTime)

	rounds = rounds - 1

