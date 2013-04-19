import random
fd = open('spiders/ip.txt','r')
data = fd.readlines()
fd.close()
length = len(data)
index  = random.randint(0, length -1)
item = data[index].strip('\n').strip(' ')
arr  = item.split(':')
print arr