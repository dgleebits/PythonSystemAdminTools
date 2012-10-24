import re
import string
import os
import shutil

alphabet = string.lowercase
path = "/Users/antigen/Downloads/"
destination = '/Users/antigen/Downloads/files'


for letter in alphabet:
    try:
        os.makedirs(path+letter, 0755)
    except:
        pass

for a,b,file in os.walk(destination):
    for item in file:
        for letter in alphabet:
            if re.search('^'+letter, item):
                shutil.copyfile(item, path+letter+"/"+item)

