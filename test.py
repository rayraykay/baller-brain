import numpy
from numpy import transpose, log, where, array
import pylab
from scipy import optimize

DATA_FILE 					= 'data.txt'
XY_VERBOSE 					= False
FULL_J_MATRIX_VERBOSE 		= False
PREDICT_ONLY_VERBOSE 		= True

BFGS_MAX_ITER				= 10000
BFGS_EPSILON				= 0.000001

LOG_DIVIDE_BY_ZERO_DEBUG	= False
X_DOT_THETA_DEBUG			= False
DEBUG_REG_CONST				= 100

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

# X is m training examples x n features
def compute_cost(theta,X,y): #computes cost given predicted and actual values
	m = X.shape[0] #number of training examples
	theta = numpy.reshape(theta,(len(theta),1))

	if (LOG_DIVIDE_BY_ZERO_DEBUG):
		print('Inside log arg:')
		print(1-sigmoid(X.dot(theta)))
	
	if (X_DOT_THETA_DEBUG):
		print('X dot theta')
		print(X.dot(theta).T)

    #y = reshape(y,(len(y),1))
	J = (1./m) * (-transpose(y).dot(log(sigmoid(X.dot(theta)))) 
			- transpose(1-y).dot(log(1-sigmoid(X.dot(theta)))))

	grad = transpose((1./m)*transpose(sigmoid(X.dot(theta)) - y).dot(X))

	if (FULL_J_MATRIX_VERBOSE):
		print(J)

	#optimize.fmin expects a single value, so cannot return grad
	return J

# WARNING: This function needs some cleaning up. It hardcodes
# some things, so that needs to be addressed
def compute_grad(theta, X, y):
	theta.shape = (1, 3)
	grad = zeros(3)
	h = sigmoid(X.dot(theta.T))

	delta = h - y
	l = grad.size
	
	for i in range(l):
		sumdelta = delta.T.dot(X[:, i])
		grad[i] = (1.0 / m) * sumdelta * - 1
		
	theta.shape = (3,)
	
	return grad

# mathematical functions
def sigmoid(X):
	denominator = 1.0 + numpy.e ** (-1*X);
	return 1/denominator

def predict(theta, X):
	m, n = X.shape
	p = numpy.zeros(shape=(m, 1))
	h = sigmoid(X.dot(theta.T))
	
	for it in range(0, h.shape[0]):
		if h[it] > 0.5:
			p[it, 0] = 1
		else:
			p[it, 0] = 0

	return p

def percentage_accuracy(X, theta, y):
	p = predict(theta, X)
	m = y.shape[0]
	correct = 0
	
	for i in range(m):
		if (y[i] == p[i]):
			correct = correct + 1
	
	return 1.0 * correct / m * 100.0

def main():
	print('Taking in data from file...')
	data = numpy.loadtxt(DATA_FILE, delimiter=',')

	# this is hardcoded in terms of dimensions, be careful
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

	# feature regularization
	X = X/DEBUG_REG_CONST

	# add constant term
	m = X.shape[0]
	ones = numpy.matrix(numpy.zeros(m)+1)
	X = numpy.concatenate((X.T, ones), axis=0)
	X = numpy.array(X.T)	

	if (PREDICT_ONLY_VERBOSE):	
		n = X.shape[1]
		init_theta = numpy.zeros(n)# + numpy.random.uniform(-1.0, 1.0, n)

		def bfgs_cost(theta):
			return compute_cost(theta, X, y)

		final_theta = optimize.fmin_bfgs(bfgs_cost, init_theta, maxiter=BFGS_MAX_ITER, epsilon=BFGS_EPSILON)
		print("The minimization has completed.")
		print("The final accuracy of the machine is: " + str(percentage_accuracy(X, final_theta, y)) + "%")

		# leftover code from the tutorial
		'''
		print(where(predict(array(final_theta),X)) == y)
		print('Final theta: ' + str(final_theta))
		print(((y[where(predict(array(final_theta),X) == y)].size / float(y.size)) * 100.0))
		'''
