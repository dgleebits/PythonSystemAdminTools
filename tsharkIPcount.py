#! /usr/bin/python

'''
This program takes a file and counts up packets to each IP address found in PCAP.
Replaces the commands below.
'''
##########
# bash way
##########
# cat test2.csv | awk {'print $5'} | sort | uniq -c

! tshark -r test.pcap -T fields -e frame.number -e eth.src -e eth.dst -e ip.src -e ip.dst -e frame.len -E header=y -E separator=" " > test2.csv
data = ! cat test2.csv


IpHitListing = {}

for line in data:
  Ip = line.split(' ')[4]
	if 6 < len(Ip) <= 15:
		IpHitListing[Ip] = IpHitListing.get(Ip,0) + 1