#!/bin/python

import socket
import leds
import sys
import random

# server port
port = 31337

CMD_DISPLAY = "display"
CMD_BROADCAST_STATE = "broadcast"
CMD_RECEIVE_STATE = "receive"
CMD_SET_NEIGHBOUR = "neighbour"
CMD_RANDOM = "random"
CMD_OFF = "off"
CMD_ON = "on"

# number of leds are defined by the number of led functions
nleds = len(leds.ledFunctions)

dr = [0, 1, 1, 1, 0, -1, -1, -1]
dc = [-1, -1, 0, 1, 1, 1, 0, -1]

randValues = []

# distributes the random states so that configurations with 2 or 3 LEDs on are more probable
for i in range(1 << nleds):
	ii = i
	bc = 0
	while ii > 0:
		if ii & 1:
			bc = bc + 1
		ii = ii >> 1
	number = nleds - abs(nleds/2 - bc)
	for j in range(number):
		randValues.append(i)
		
def nextRand():
	return randValues[random.randint(0, len(randValues)-1)]

neighbourIp = ["", ""]
host = ""

state = [[0,0,0], [0,0,0]] # double buffer flipping back and forth; idx 0 and 2 are neighbours, idx 1 is this router
stateIdx = 0
updateCount = 0

size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))


def printBoard(board):
	for r in board:
		for c in range(nleds):
			if (r & (1 << c)) != 0:
				sys.stdout.write('x')
			else:
				sys.stdout.write('.')
		sys.stdout.write('\n')
	
def reset(state):
#	rand = random.randint(0, 1 << len(leds.ledFunctions))
	rand = nextRand()
	state[0] = [0, rand, 0]
	state[1] = [0, 0, 0]
	
reset(state)
stateIdx = 1
#printBoard(state[0])
	
while 1:
	data, address = s.recvfrom(size)
	
	split = data.split()
	
	if split[0] == CMD_OFF:
		print "off"
		for r in range(nleds):
			leds.ledFunctions[r](0)
	
	if split[0] == CMD_ON:
		print "on"
		for r in range(nleds):
			leds.ledFunctions[r](1)

	if split[0] == CMD_DISPLAY:
		print "display"
#		printBoard(state[stateIdx])
		
		for r in range(nleds):
			ledOn = state[stateIdx][1] & (1 << r)
			leds.ledFunctions[r](0 if ledOn == 0 else 1)
			
		stateIdx = 1 - stateIdx
		updateCount = 0
			
	elif split[0] == CMD_BROADCAST_STATE:
		print "broadcast"
		for ip in filter(lambda x : len(x) != 0, neighbourIp):
#			print "- sending to", ip
			s.sendto(" ".join([CMD_RECEIVE_STATE, str(state[1-stateIdx][1])]), (ip, port))
		
	elif split[0] == CMD_RECEIVE_STATE:
		print "receive from", address[0]
		hit = False
		
		for i in range(2):
			if address[0] == neighbourIp[i]:
				state[1-stateIdx][2 * i] = int(split[1]) # idx is either 0 or 2
				hit = True
				break
		
		if hit:
			updateCount = updateCount + 1
			
			if updateCount == neighbours:
#				print "- BEFORE"
#				printBoard(state[1-stateIdx])
				
				# update!
#				print "- next generation!"
				state[stateIdx][1] = 0
				
				for r in range(nleds):
					ledOn = (state[1-stateIdx][1] & (1 << r)) != 0
					liveCount = 0
					for j in range(8):
						if r+dr[j] < 0:
							continue
						ledOn2 = state[1-stateIdx][1+dc[j]] & (1 << (r+dr[j]))
						if ledOn2:
							liveCount = liveCount + 1
					
					if ledOn and (liveCount == 2 or liveCount == 3):
						state[stateIdx][1] |= (1 << r)
					elif not ledOn and liveCount == 3:
						state[stateIdx][1] |= (1 << r)
		
#				print "- AFTER"
#				printBoard(state[stateIdx])
				
	elif split[0] == CMD_SET_NEIGHBOUR:
		print "neighbour"
		id = int(split[1])
		neighbourIp[id] = split[2]
		
		neighbours = len(filter(lambda x : len(x) != 0, neighbourIp))
		
	elif split[0] == CMD_RANDOM:
		print "random"
		reset(state)
		stateIdx = 1
#		printBoard(state[0])
		
	else:
		print "unknown"

