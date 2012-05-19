#/usr/bin/python
'''
This program rips thru text dumps of NMAP text output and puts it into a pickled datafile for PythonPandas analysis
'''

import re
import cPickle as pickle
import datetime

data = ! cat *
newDict = {}
newList = []
splitLine = ['0.0.0.0','0.0.0.0']
pattern = re.compile('[0-9]{1,5}/tcp')
nowTime = datetime.datetime.now().strftime('%Y-%m-%d')

for line in data:
	if 'Nmap scan report for ' in line:
		cutLine = line[21:]
		splitLine = cutLine.split(' ')
		if len(splitLine) == 1:
			splitLine.insert(1, splitLine[0])
		if len(splitLine) == 2:
			asdf = splitLine[1].lstrip('(')
			asdf = asdf.rstrip(')')
		splitLine.insert(1, asdf)
		splitLine.pop()

	match = pattern.search(line)
	if match: # looking for listings of open ports
		newList.append(match.group())

	if len(line) == 0: # this is the end scan object and creates a DICT with all the objects
		newDict [splitLine[0]]=[splitLine[1],newList]
		newList = []

# saving pickled file to disk
pickle.dump( newDict, open( "saveNewDict."+nowTime, "wb", True ) )