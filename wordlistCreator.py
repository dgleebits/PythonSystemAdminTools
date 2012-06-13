alphabet='abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
upperAlpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

with open("test2.txt", "a") as myfile:

	for l1 in alphabet:
		final1 = l1+'\n'
		myfile.write(final1)
		
		for l2 in alphabet:
			final2 = l1+l2+'\n'
			myfile.write(final2)
			
			for l3 in alphabet:
				final3 = l1+l2+l3+'\n'
				myfile.write(final3)
				
				for l4 in alphabet:
					final4 = l1+l2+l3+l4+'\n'
					myfile.write(final4)
					
					for l5 in alphabet:
						final5 = l1+l2+l3+l4+l5+'\n'
						myfile.write(final5)
						
						for l6 in alphabet:
							final6 = l1+l2+l3+l4+l5+l6+'\n'
							myfile.write(final6)
							
							for l7 in alphabet:
								final7 = l1+l2+l3+l4+l5+l6+l7+'\n'
								myfile.write(final7)
								
								for l8 in alphabet:
									final8 = l1+l2+l3+l4+l5+l6+l7+l8+'\n'
    									myfile.write(final8)

import hashlib
fh = open ('test2.txt')
fw = open ('sha1Hashed.txt', 'w')
for i in range(10000):
    password = fh.readline().strip()
    hex = hashlib.sha1(password).hexdigest()
    fw.write(password+','+hex+'\n')
fh.close
fw.close
'''
# terrible code to generate 8 char wordlist


alphabet='abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'

for l1 in alphabet:
  for l2 in alphabet:
		for l3 in alphabet:
			for l4 in alphabet:
				for l5 in alphabet:
					for l6 in alphabet:
						for l7 in alphabet:
							for l8 in alphabet:
								final1 = l1+'\n'
								final2 = l1+l2+'\n'
								final3 = l1+l2+l3+'\n'
								final4 = l1+l2+l3+l4+'\n'
								final5 = l1+l2+l3+l4+l5+'\n'
								final6 = l1+l2+l3+l4+l5+l6+'\n'
								final7 = l1+l2+l3+l4+l5+l6+l7+'\n'
								final8 = l1+l2+l3+l4+l5+l6+l7+l8+'\n'
								with open("test.txt", "a") as myfile:
    								myfile.write(final1)
    								myfile.write(final2)
    								myfile.write(final3)
    								myfile.write(final4)
    								myfile.write(final5)
    								myfile.write(final6)
    								myfile.write(final7)
    								myfile.write(final8)
    								
    								'''
    								