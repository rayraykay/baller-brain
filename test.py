import numpy
import pylab

data_file = 'data.txt'

if __name__=="__main__":
	print('Taking in data from file...')
	data = numpy.loadtxt(data_file, delimiter=',')
	print(data)

	x = data[:, 0:2]
	y = data[:, 2]

	print('Printing out data for x and y...')	
	print('x: ')
	print(str(x))
	print('y: \n' + str(y))

	pos = numpy.where(y == 1)
	neg = numpy.where(x == 0)
