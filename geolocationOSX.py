#!/usr/bin/env python
# Julien Deudon (initbrain) - 20/03/2012 15h35
# modified to english version by Dan Gleebits 20/06/2012
# modified to run on OS X by James Armitage 25/06/2012
# modified to process in python Dan Gleebits 26/06/2012
# parsing xml Vincent Ohprecio 01/10/2012

from commands import getoutput
import re, urllib2, webbrowser
import json as simplejson
import xml.etree.ElementTree as ET

airport_scan_xml = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan -x'
address_match = '([a-fA-F0-9]{1,2}[:|\-]?){6}'

def get_signal_strengths():
    signal_by_address = {}
    root = ET.fromstring(getoutput(airport_scan_xml))
    networks = root.getchildren()[0]

    for network in networks:
        # First "string" child is MAC address
        address = network.find("string").text
        # Eighth "integer" is signal strength
        strength = abs(int(network.findall("integer")[7].text))
        signal_by_address[address] = strength

    return signal_by_address

def convert_dict_to_json(signal_by_address):
    location_request = {
        "version": "1.1.0",
        "request_address": False,
        "wifi_towers": [],
        }

    for address, signal in signal_by_address.items():
        tower = {"mac_address": address, "signal_strength": signal}
        location_request["wifi_towers"].append(tower)

    return simplejson.JSONEncoder().encode(location_request)

def post_json_and_get_lat_long(json):
    output = simplejson.loads(urllib2.urlopen('https://www.google.com/loc/json', json).read())

    return output["location"]["latitude"], output["location"]["longitude"]


if __name__ == "__main__":
    print "[+] Scanning network"
    signal_by_address = get_signal_strengths()

    json = convert_dict_to_json(signal_by_address)

    print "[+] Sending the request to Google"
    loc = post_json_and_get_lat_long(json)

    map_url = "http://maps.google.com/maps?q=%s,%s" % loc
    print "[+] Google Map"
    print map_url

    webbrowser.open(map_url)
