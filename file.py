import json
# Using readline()
file1 = open('pubmed-dataset/train.txt', 'r')
count = 0
train, val, test = [],[],[]


while count < 80:
	count += 1
	line = file1.readline()
	train.append(line)

while count >=80 and count < 90:
	count += 1
	line = file1.readline()
	val.append(line)

while count >=90 and count < 100:
	count += 1
	line = file1.readline()
	test.append(line)
file1.close()


file2 = open('train.txt', 'w')
file2.writelines((train))
file2.close()

file2 = open('validation.txt', 'w')
file2.writelines((val))
file2.close()

file2 = open('test.txt', 'w')
file2.writelines((test))
file2.close()