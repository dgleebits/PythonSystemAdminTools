#!/usr/bin/env python
'''
This program is for finding words out of lists or books that end or being with certain letters or numbers of basic patterns
'''

data = open ("namesFoundOnInternet.txt").readlines()

#process each line and strip return characters
#append each work matching "end with s"
#create mylist filled with words ending in s
for line in data:
    b = list(line.strip())
    if b[-1] == "s":
        mylist.append(line)
fout = open ('names.txt', 'w')
for line in mylist:
    fout.write(line)
fout.close()

#process each line and strip return characters
#append each work matching "begin with c"
#create mylist filled with words begin with c
mylist2=[]
for line in mylist:
    b = list(line.strip())
    if b[0] == "c":
        mylist2.append(line)

fout = open ('names2.txt', 'w')
for line in mylist2:
    fout.write(line)
fout.close()
