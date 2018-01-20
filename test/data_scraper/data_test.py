import get_data
import numpy
import pylab

def show_logistic_graph(X, xlabel, ylabel, legend, pos, neg):
	pylab.scatter(X[pos, 0], X[pos, 1], marker='o', c='b')
	pylab.scatter(X[neg, 0], X[neg, 1], marker='x', c='r')
	pylab.xlabel(xlabel)
	pylab.ylabel(ylabel)
	pylab.legend(legend)
	pylab.show()



if __name__=="__main__":
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
	print(X)

