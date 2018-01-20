import numpy
import pylab
from scipy import optimize

DATA_FILE = 'data.txt'
XY_VERBOSE = False

def show_logistic_graph(X, xlabel, ylabel, legend):
	pylab.scatter(X[pos, 0], X[pos, 1], marker='o', c='b')
	pylab.scatter(X[neg, 0], X[neg, 1], marker='x', c='r')
	pylab.xlabel('Exam 1 score')
	pylab.ylabel('Exam 2 score')
	pylab.legend(['Not Admitted', 'Admitted'])
	pylab.show()

def bfgs_test(func, init_x):
	return optimize.fmin_bfgs(func, init_x)

def func_x_squared(x):
	return x ** 2;

# mathematical functions
def sigmoid(X):
	denominator = 1.0 + numpy.e ** (-1*X);
	return 1/denominator

if __name__=="__main__":
	print('Taking in data from file...')
	data = numpy.loadtxt(DATA_FILE, delimiter=',')

	X = data[:, 0:2]
	y = data[:, 2]

	if (XY_VERBOSE):
		print(data)
		print('Printing out data for x and y...')	
		print('x: ')
		print(str(X))
		print('y: \n' + str(y))

	pos = numpy.where(y == 1)
	neg = numpy.where(y == 0)
	
	legend = ['Not Admitted', 'Admitted']
	xlabel = 'Exam 1 Score'
	ylabel = 'Exam 2 Score'
	show_logistic_graph(X, xlabel, ylabel, legend)
	
	test_min = bfgs_test(func_x_squared, 1)
