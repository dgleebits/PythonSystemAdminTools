#! /usr/bin/python
'''
ALPHA Program takes PCAP files that have been converted by ***tshark -V -r infile.pcap > outputfile.txt***
and creates comma separated (csv) file
'''

import sys
import os
import re
import datetime


fh = open('outputfile.txt')
data = fh.readlines()

fn = '    Frame Number: '
fl = '    Frame Length: '
src = '        Source: '
dest = '    Destination: '
srcPort = ' Src Port: '
destPort = ' Dst Port: '
seqNum = ' Seq: '
ack = ' Ack: '
lenPacket = ' Len: '

for line in data:
  if 'Frame Number:' in line:
		print line
	if 'Frame Length:' in line:
		print line
	if 'Source:' in line:
		print line
	if 'Destination:' in line:
		print line
	if 'Transmission Control Protocol, Src Port: ' in line:
		stats = line.split(',')
		for item in stats:
			if srcPort in item:
				print item[len(srcPort):]
			if destPort in item:
				print item[len(destPort):]
			if seqNum in item:
				print item[len(seqNum):]
			if ack in item:
				print item[len(ack):]
			if lenPacket in item:
				print item[len(lenPacket):]

testdata = '''
Frame 1486: 60 bytes on wire (480 bits), 60 bytes captured (480 bits)
    Arrival Time: May 10, 2012 21:44:46.146028000 PDT
    Epoch Time: 1336711486.146028000 seconds
    [Time delta from previous captured frame: 2.139154000 seconds]
    [Time delta from previous displayed frame: 2.139154000 seconds]
    [Time since reference or first frame: 714.744465000 seconds]
    Frame Number: 1486
    Frame Length: 60 bytes (480 bits)
    Capture Length: 60 bytes (480 bits)
    [Frame is marked: False]
    [Frame is ignored: False]
    [Protocols in frame: eth:ip:igmp]
Ethernet II, Src: CiscoSpv_df:58:a4 (48:44:87:df:58:a4), Dst: IPv4mcast_6f:00:05 (01:00:5e:6f:00:05)
    Destination: IPv4mcast_6f:00:05 (01:00:5e:6f:00:05)
        Address: IPv4mcast_6f:00:05 (01:00:5e:6f:00:05)
        .... ...1 .... .... .... .... = IG bit: Group address (multicast/broadcast)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
    Source: CiscoSpv_df:58:a4 (48:44:87:df:58:a4)
        Address: CiscoSpv_df:58:a4 (48:44:87:df:58:a4)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
    Type: IP (0x0800)
    Trailer: 0000000000000000000000000000
Internet Protocol Version 4, Src: 192.168.1.64 (192.168.1.64), Dst: 232.239.0.5 (232.239.0.5)
    Version: 4
    Header length: 24 bytes
    Differentiated Services Field: 0xa0 (DSCP 0x28: Class Selector 5; ECN: 0x00: Not-ECT (Not ECN-Capable Transport))
        1010 00.. = Differentiated Services Codepoint: Class Selector 5 (0x28)
        .... ..00 = Explicit Congestion Notification: Not-ECT (Not ECN-Capable Transport) (0x00)
    Total Length: 32
    Identification: 0xe0b6 (57526)
    Flags: 0x00
        0... .... = Reserved bit: Not set
        .0.. .... = Don't fragment: Not set
        ..0. .... = More fragments: Not set
    Fragment offset: 0
    Time to live: 1
    Protocol: IGMP (2)
    Header checksum: 0x98a4 [correct]
        [Good: True]
        [Bad: False]
    Source: 192.168.1.64 (192.168.1.64)
    Destination: 232.239.0.5 (232.239.0.5)
    Options: (4 bytes)
        Router Alert: Every router examines packet
Internet Group Management Protocol
    [IGMP Version: 2]
    Type: Membership Report (0x16)
    Max Response Time: 0.0 sec (0x00)
    Header checksum: 0x010b [correct]
    Multicast Address: 232.239.0.5 (232.239.0.5)

Frame 1487: 1484 bytes on wire (11872 bits), 1484 bytes captured (11872 bits)
    Arrival Time: May 10, 2012 21:44:47.078486000 PDT
    Epoch Time: 1336711487.078486000 seconds
    [Time delta from previous captured frame: 0.932458000 seconds]
    [Time delta from previous displayed frame: 0.932458000 seconds]
    [Time since reference or first frame: 715.676923000 seconds]
    Frame Number: 1487
    Frame Length: 1484 bytes (11872 bits)
    Capture Length: 1484 bytes (11872 bits)
    [Frame is marked: False]
    [Frame is ignored: False]
    [Protocols in frame: eth:ip:udp:data]
Ethernet II, Src: CiscoSpv_df:58:a4 (48:44:87:df:58:a4), Dst: IPv4mcast_7f:ff:fa (01:00:5e:7f:ff:fa)
    Destination: IPv4mcast_7f:ff:fa (01:00:5e:7f:ff:fa)
        Address: IPv4mcast_7f:ff:fa (01:00:5e:7f:ff:fa)
        .... ...1 .... .... .... .... = IG bit: Group address (multicast/broadcast)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
    Source: CiscoSpv_df:58:a4 (48:44:87:df:58:a4)
        Address: CiscoSpv_df:58:a4 (48:44:87:df:58:a4)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
        .... ..0. .... .... .... .... = LG bit: Globally unique address (factory default)
    Type: IP (0x0800)
Internet Protocol Version 4, Src: 192.168.1.64 (192.168.1.64), Dst: 239.255.255.250 (239.255.255.250)
    Version: 4
    Header length: 20 bytes
    Differentiated Services Field: 0xa0 (DSCP 0x28: Class Selector 5; ECN: 0x00: Not-ECT (Not ECN-Capable Transport))
        1010 00.. = Differentiated Services Codepoint: Class Selector 5 (0x28)
        .... ..00 = Explicit Congestion Notification: Not-ECT (Not ECN-Capable Transport) (0x00)
    Total Length: 1470
    Identification: 0xe0b7 (57527)
    Flags: 0x00
        0... .... = Reserved bit: Not set
        .0.. .... = Don't fragment: Not set
        ..0. .... = More fragments: Not set
    Fragment offset: 0
    Time to live: 1
    Protocol: UDP (17)
    Header checksum: 0x20f5 [correct]
        [Good: True]
        [Bad: False]
    Source: 192.168.1.64 (192.168.1.64)
    Destination: 239.255.255.250 (239.255.255.250)
User Datagram Protocol, Src Port: neod2 (1048), Dst Port: us-cli (8082)
    Source port: neod2 (1048)
    Destination port: us-cli (8082)
    Length: 1450
    Checksum: 0x7a43 [validation disabled]
        [Good Checksum: False]
        [Bad Checksum: False]
Data (1442 bytes)
'''

########################################### to do ###############################	
#		
#need re for ip address
# '((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])'
#
#need re for mac address
# '([0-9A-F]{2}[:-]){5}([0-9A-F]{2})'
#
#need to make test module
# 
# ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
#
# ValidHostnameRegex = "^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$";


'''
import re, urllib2

ips = re.findall('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', page)
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)
emails = re.findall('[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', page)
page = ''.join( urllib2.urlopen('http://www.example.com/index.html').readlines() )

def date_from_filename (filename):
    m = re.match(".*?[0-9]{2}-(?P<YEAR>[0-9]{4})(?P<MONTH>[0-9]{2})(?P<DAY>[0-9]{2})(?P<HOUR>[0-9]{2})(?P<MIN>[0-9]{2})(?P<SEC>[0-9]{2})-(?P<SEQ>[0-9]{2}).*?", filename)
    if m is None:
        print "Bad date parse in filename:", filename
        return None
    day   = int(m.group('DAY'))
    month = int(m.group('MONTH'))
    year  = int(m.group('YEAR'))
    hour  = int(m.group('HOUR'))
    min   = int(m.group('MIN'))
    sec   = int(m.group('SEC'))
    dts = (year, month, day, hour, min, sec, 0, 1, -1)
    return dts
	
re.search ("(?is)username.*?password", string)
'''
		