#!/usr/bin/env python
# Julien Deudon (initbrain) - 20/03/2012 15h35
# modified to english version by Dan Gleebits 20/06/2012
# modified to run on OS X by James Armitage 25/06/2012
# modified to pure python Dan Gleebits 26/06/2012

from commands import getoutput
import sys, re, simplejson, urllib2, webbrowser

macAddress = ''
signalStrength = 0
locationRequest = {}
path2WiFi = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport scan'

# running network WiFi scan
print "[+] Scanning network"
neighborWiFi = getoutput(path2WiFi)
neighborWiFi = neighborWiFi.split('\n')
neighborWiFi = neighborWiFi[1:len(neighborWiFi)]

print "[+] Creating HTML request"
locationRequest={ 
		"version":"1.1.0",
		"request_address":False, 
		"wifi_towers":[{"mac_address":x.split()[1].replace(":","-"),"signal_strength":abs(int(x.split()[2]))} for x in neighborWiFi]
		}
				
print "[+] Sending the request to Google"
data = simplejson.JSONEncoder().encode(locationRequest)
output = simplejson.loads(urllib2.urlopen('https://www.google.com/loc/json', data).read())

print "[+] Google Map"
print "http://maps.google.com/maps?q="+str(output["location"]["latitude"])+","+str(output["location"]["longitude"])
googleMapWebpage = "http://maps.google.com/maps?q="+str(output["location"]["latitude"])+","+str(output["location"]["longitude"])
webbrowser.open(googleMapWebpage)
