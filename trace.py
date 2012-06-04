#!/usr/bin/env python

'''
Copyright (C) 2011 by Sebastien Goasguen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import subprocess
import networkx as nx
import socket
import sys
import os
import re
import getopt
import json
import datetime
import pprint

'''Need to be root to use scapy'''
import scapy
from scapy.all import *

'''Needed to plot the graph, otherwise skip'''
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

'''Needed to keep a store of all targets
Requires to run a mongodb server on your machine
'''
import pymongo
from pymongo import Connection

def setup_db():
  '''Needs mongodb to store targets as dictionaries'''
	try:
		dbconn=Connection()
	except:
		print "Could not connect to db, make sure you started mongo"
	try:
		db=dbconn.pentest
	except:
		print "Could not get the pentest database"

	try:
		collection=db.targets
	except:
		print "Could not get the collection of targets"

	return collection

def get_all_targets():
	'''Retruns all targets stored in the database'''
	for t in coll.find():
		pprint.pprint(t,indent=4)

class target():
	'''Create a target class based on a dictionary
	Stored in a mongodb document store
	IP input is assumed to be a tuple returned by bruteforce_reversedns call
	Needs to be improved
	'''
	def __init__(self,ip,coll=None):
		self.target={}
		self.ip=ip[0]
		self.target['hostname']=ip[1]
		self.collection=coll

	def __str__(self):
		'''Uses json to do a pretty print of the target dictionary'''
		return json.dumps(self.target,sort_keys=True,indent=4)
	
	def make_target(self):
		'''Populates the target dictionary and stores it in a database of targets'''
		self.target_ip()
		self.port_scanned()
		self.traceroute()
		self.target['Timestamp']=str(datetime.datetime.utcnow())
		self.collection.insert(self.target)

	def target_ip(self):
		'''Sets the IP in the dictionary'''
		self.target['ip']=self.ip

	def port_scanned(self):
		''''Sets the open/closed/filtered ports for that target based on a basic nmap scan 
		and inserts it in the dictionary'''
		ports=nmap_scan(self.ip)
		self.target['ports']=ports

	def traceroute(self):
		'''Runs a scapy TCP traceroute and inserts it in the dictionary'''
		hops=scapytraceroute(self.ip)
		self.target['traceroute']=hops

def bruteforce_reversedns(base_ip):
	'''Gets hostnames registered in DNS from IP range, takes Class C as input
	i.e 130.127.39.	Would be nice to do a proper CIDR notation
	Could try to do DNS requests in scapy	
	'''
	ip_list=[]
	for i in range(255):
		try:
			(hostname,alias,ip)=socket.gethostbyaddr(base_ip+str(i))
			ip_list.append((ip[0],hostname))
		except:
			pass

	return	ip_list

def nmap_scan(host):
	'''Calls nmap with a subprocess to get the list of open ports
	Uses a Syn scan, edit the cmd string to your needs and taste.
	Returns a list of ports via basic regular expression of nmap output
	Could be improved using nmap xml output and proper xml parsing
	'''
	ports = []
	cmd = 'sudo nmap -Pn -sS ' + host
	print 'Scanning: ' + cmd
	p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(pout,perr)=p.communicate()

	foobar=re.compile('tcp')
	for line in pout.split('\n'):
		if foobar.search(line):
			print line
			ports.append(line)
	return ports

def localtraceroute(host,num_hops):
	'''Calls traceroute via subprocess, needs host and the number of hops as arguments
	Edit the trace string to your needs and taste, it returns a list of hops	
	'''
	hops=[]
	trace='traceroute -m %d %s' % (num_hops,host)
	print trace
	res=subprocess.Popen(trace,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(pstdout,psterr)=res.communicate()
	lines=pstdout.split('\n')
	for line in lines[:num_hops]:
		hops.append(line.split(' ')[num_hops-1].rstrip(')').lstrip('('))
	return hops

def scapytraceroute(host):
	'''Uses scapy to do a tcp traceroute hopefully goes through firewalls
	Returns a list of hops
	'''
	hops=[]
	try:
		res,unans=traceroute(host)
	except:
		print "Could not trace route with scapy !"
		return hops
	
	host_key=res.get_trace().keys()[0]

	for key in res.get_trace()[host_key].keys():
		hops.append(res.get_trace()[host_key][key][0])
		
	return hops

def traceroute_plot(targets):
	'''Plots the graph of the traceroutes for a list of IP targets
	Calls the scapytraceroute.
	'''
	g=nx.Graph()
	source=socket.gethostbyname(socket.gethostname())
	
	for t in targets:
		hops=scapytraceroute(t)
		print hops

		g.add_node(t)
		g.add_edge(source,hops[0])

		if len(hops) >= 1:
			for hop in hops:
				next_hop_index=hops.index(hop)+1
				if next_hop_index != len(hops):
					g.add_edge(hop,hops[next_hop_index])
				else:
					g.add_edge(hop,t)

	nx.draw(g,with_labels=False)
	plt.savefig("/Users/runseb/Desktop/481_f2011/trace.png")
	nx.write_dot(g,"/Users/runseb/Desktop/481_f2011/trace.dot")

def traceroute_plot_from_db(targets):
	'''Assumes that if a target is in the db then the traceroute has already been run
	The targets input is a list of dictionaries from the db	instead of IPs only.
	'''
	g=nx.Graph()
	source=socket.gethostbyname(socket.gethostname())
	
	for t in targets:
		hops=t['traceroute']
		print hops

		g.add_node(t['ip'])
		g.add_edge(source,hops[0])

		if len(hops) >= 1:
			for hop in hops:
				next_hop_index=hops.index(hop)+1
				if next_hop_index != len(hops):
					g.add_edge(hop,hops[next_hop_index])
				else:
					g.add_edge(hop,t['ip'])

	nx.draw(g,with_labels=False)
	plt.savefig("/Users/runseb/Desktop/481_f2011/trace.png")
	nx.write_dot(g,"/Users/runseb/Desktop/481_f2011/trace.dot")

def main():
	'''Main function'''
	targets=[]

	try:
		fh=open(targets_file,'r')
	except:
		print "targets.list file not present"
		sys.exit()

	for line in fh.readlines():
		targets.append(line.strip('\n'))

	traceroute_plot(targets)
	
def readopt():
	''' Uses getopt to read the input arguments/options '''
	''' Should be improve to specify file of targets '''
	try:
		options, remainder = getopt.getopt(sys.argv[1:],'b:s:t:f:')
	except getopt.GetoptError, err:
		print str(err)
	        usage()
        	sys.exit(2)

	'''Set defaults'''
	global base_ip,host_to_scan,host_to_traceroute,targets_file
	base_ip = '127.0.0'
	host_to_scan = '127.0.0.1'
	host_to_traceroute = '127.0.0.1'
	targets_file = 'targets.list'

	for opt, arg in options:
		if opt == '-b':
			base_ip = arg
		elif opt == '-s':
			host_to_scan = arg
		elif opt == '-t':
			host_to_traceroute == arg
		elif opt == '-f':
			targets_file == arg
		else:
			usage()
			sys.exit(2)
def usage():
	'''Prints the input arguments options if you run the code directly'''
	print "This code plots the traceroute to a set of hosts"

if __name__=="__main__":
	readopt()
	sys.exit(main())
else:
	print "The db setup will called and can be refered as trace.coll() in an interactive shell"	
	coll=setup_db()
