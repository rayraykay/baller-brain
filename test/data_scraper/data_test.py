import get_data
import numpy
import pylab
import test

from scipy import optimize

def show_logistic_graph(X, xlabel, ylabel, legend, pos, neg):
	pylab.scatter(X[pos, 0], X[pos, 1], marker='o', c='b')
	pylab.scatter(X[neg, 0], X[neg, 1], marker='x', c='r')
	pylab.xlabel(xlabel)
	pylab.ylabel(ylabel)
	pylab.legend(legend)
	pylab.show()

if __name__=="__main__":
	print(optimize.fmin_bfgs(test.func_x_squared, 1))	
	data = get_data.feature_matrix()
	data = numpy.array(data)

	# this is hardcoded in terms of dimensions, be careful
	X = data[:, 0:2]
	y = data[:, 2]

	pos = numpy.where(y == 1)
	neg = numpy.where(y == 0)
	
	legend = ['Away Team Won', 'Home Team Won']
	xlabel = 'Away Team Points-to-Points Against Ratio'
	ylabel = 'Home Team Points-to-Points Against Ratio'
	show_logistic_graph(X, xlabel, ylabel, legend, pos, neg)		

	m = X.shape[0]
	ones = numpy.matrix(numpy.zeros(m)+1)
	X = numpy.concatenate((ones, X.T), axis=0)
	X = numpy.array(X.T)
	
	# test prediction
	n = X.shape[1]
	init_theta = numpy.zeros(n)

	def bfgs_cost(theta):
		test.compute_cost(theta, X, y)
	
	print(X)
	print(y)
	print(init_theta)
	print(test.compute_cost(init_theta,X,y))
	
	final_theta = optimize.fmin_bfgs(bfgs_cost, init_theta, maxiter=10000, epsilon=0.001)
	print("The minimization has completed.")
	print("The final accuracy of the machine is: " + str(percentage_accuracy(X, final_theta, y)) + "%")


