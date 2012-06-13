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