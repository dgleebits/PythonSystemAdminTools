#!/usr/bin/env python
# Julien Deudon (initbrain) - 20/03/2012 15h35
# modified to english version by Dan Gleebits 20/06/2012
# modified to run on OS X by James Armitage 25/06/2012
# modified to process in python Dan Gleebits 26/06/2012
# commented all the file for Dan. Vincent Ohprecio 01/10/2012

# import all the necessary libraries
from commands import getoutput
import re, urllib2, webbrowser
import json as simplejson

# bash command to grab the neighboring wifi data around the laptop
path2WiFi = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport scan'

# regular expression to match MAC address
macMatch = '([a-fA-F0-9]{2}[:|\-]?){6}'
count = 0

# running network WiFi scan
print "[+] Scanning network"
neighborWiFi = getoutput(path2WiFi)
neighborWiFi = neighborWiFi.split('\n')

# cleaning up bad data		
for line in neighborWiFi:
	a = re.compile(macMatch).search(line)
	if a:
		count +=1
	else:
		neighborWiFi.pop(count)
		
print "[+] Creating HTML request"
locationRequest={
		"version":"1.1.0",
		"request_address":False, 
		"wifi_towers":[{"mac_address":"00-00-00-00-00-00","signal_strength":0}],
		}

# this is cleaning up the data file splitting the data into MAC Address and Signal Strength				
for x in neighborWiFi:
    a = re.compile(macMatch).search(x.split()[1])
    b = re.compile(macMatch).search(x.split()[2])
    if a:
        tempDict = {"mac_address":x.split()[1].replace(":","-"),"signal_strength":abs(int(x.split()[2]))}
        locationRequest["wifi_towers"].append(tempDict)
    elif b:
        tempDict = {"mac_address":x.split()[2].replace(":","-"),"signal_strength":abs(int(x.split()[3]))}
        locationRequest["wifi_towers"].append(tempDict)
           
# this takes the cleaned up data and serialize to JSON request for Google API
print "[+] Sending the request to Google"
data = simplejson.JSONEncoder().encode(locationRequest)
output = simplejson.loads(urllib2.urlopen('https://www.google.com/loc/json', data).read())

# prints out the latitude and longitute data returned from Google and opens browser to visually location MAC
print "[+] Google Map"
print "http://maps.google.com/maps?q="+str(output["location"]["latitude"])+","+str(output["location"]["longitude"])
googleMapWebpage = "http://maps.google.com/maps?q="+str(output["location"]["latitude"])+","+str(output["location"]["longitude"])
webbrowser.open(googleMapWebpage)
