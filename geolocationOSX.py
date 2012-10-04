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

def get_bssid_signal_strength():
    signal_by_address = {}
    root = ET.fromstring(getoutput(airport_scan_xml))

    for level_1 in root:
        for level_2 in level_1:
            for level_3 in level_2.findall('string'):
                if re.compile(address_match).search(level_3.text):
                    mac_address = level_3.text
            for level_3 in level_2:
                if level_3.text == None:
                    pass
                else:
                    if len(level_3.text) < 6 and len(level_3.text) > 1:
                        if "NOISE" in level_3.text:
                            flag = 2
                        if "RSSI" in level_3.text:
                            flag = 1
                        if len(level_3.text) < 4:
                            try:
                                signal_number = int(level_3.text)
                                if signal_number < 0:
                                    final_signal_strength = abs(int(level_3.text))
                                if flag == 1:
                                    signal_strength = final_signal_strength
                            except:
                                pass
                        if "SSID" == level_3.text:
                            flag = 0
            signal_by_address[mac_address] = signal_strength

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
    signal_by_address = get_bssid_signal_strength()

    json = convert_dict_to_json(signal_by_address)

    print "[+] Sending the request to Google"
    loc = post_json_and_get_lat_long(json)

    map_url = "http://maps.google.com/maps?q=%s,%s" % loc
    print "[+] Google Map"
    print map_url

    webbrowser.open(map_url)
