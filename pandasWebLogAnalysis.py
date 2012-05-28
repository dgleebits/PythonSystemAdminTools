#! /usr/bin/python
'''
This program uses pandas to load logs into DataFrame for analysis
'''
import pandas
data = open('www-media.log').readlines()
frame = pandas.DataFrame([x.split() for x in data])

countIP = frame[0].value_counts()
countRequested = frame[6].value_counts()
countReferal = frame[10].value_counts()

print countIP
print countRequested
print countReferal

def get_bruteRoot(data):
  for line in data:
		if 'Failed password for root' in line:
			mylist.append(line)
	frame = pandas.DataFrame([x.split() for x in mylist])
	return frame[10].value_counts()
	
def get_brute2(data, searchTerm):
	for line in data:
		if 'Failed password for '+searchTerm in line:
			mylist.append(line)
	frame = pandas.DataFrame([x.split() for x in mylist])
	return frame[10].value_counts()

def get_failedPasswordInvalidUser(data):
	for line in data:
		if 'Failed password for invalid user' in line:
			mylist.append(line)
	failedframe = pandas.DataFrame([x.split() for x in mylist])
	return failedframe[10].value_counts()
		
def get_loginHistory(data):
	for line in data:
		if 'Failed password for' in line:
			mylist.append(line)
	frame = pandas.DataFrame([x.split() for x in mylist])
	return frame[8].value_counts()