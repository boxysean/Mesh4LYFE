#!/bin/python

import os
import sys
import time

def powerGreen(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/wndr3700:green:power/brightness"))
	
def powerOrange(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/wndr3700:orange:power/brightness"))

def usbGreen(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/wndr3700:green:usb/brightness"))
	
def wanGreen(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/wndr3700:green:wan/brightness"))
	
def wpsGreen(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/wndr3700:green:wps/brightness"))
	
def wireless24Green(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/ath9k-phy0/brightness"))
	
def wireless51Blue(value):
	os.system("echo %d > %s" % (value, "/sys/class/leds/ath9k-phy1/brightness"))
	
ledFunctions = [powerGreen, wireless24Green, wireless51Blue, usbGreen]
	
if __name__ == "__main__":
	i = 0
	while 1:
		i = i + 1
		for j in [powerGreen, wireless24Green, wireless51Blue, usbGreen]:
			j(i&1)
			time.sleep(0.1)
