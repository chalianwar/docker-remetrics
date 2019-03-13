
import numpy

data = numpy.loadtxt('pull_count_sorted.csv', delimiter = ',', dtype = str)
print data
numrows = len(data)
numcols = len(data[0])

unique_name = []
unique_arry = [] #numpy.zeros(shape=(numrows, numcols))
fout = open('unique_name.txt', 'w+')
for i in range(numrows):
	if data[i][numcols - 1] not in unique_name:
		unique_arry.append(data[i,:])
		for j in range(numcols):
			fout.writelines(data[i,j])
			fout.writelines(',')
		fout.writelines('\n')
		unique_name.append(data[i][numcols - 1])

out = numpy.array(unique_arry)
fout.close()
numpy.savetxt('unique_name.out', out, fmt = "%s,%s,%s")
