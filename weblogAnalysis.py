#! /usr/bin/python
'''
This program takes in a apache www-media.log and provides basic report
'''

for collections import Counters

ipAddressList = []
methodList = []
requestedList = []
referalList = []
mylist = []

data = open('www-media.log').readlines()
for line in data:
  ipAddressList.append(line.split()[0])
	requestedList.append(line.split()[6])
	methodList.append(line.split()[5])
	referalList.append(line.split()[10])

count_ip = Counter(ipAddressList)
count_requested = Counter(requestedList)
count_method = Counter(methodList)
count_referal = Counter(referalList)

count_ip.most_common()
count_requested.most_common()
count_method.most_common()
count_referal.most_common()