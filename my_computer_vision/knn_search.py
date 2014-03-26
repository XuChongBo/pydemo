from numpy import random,argsort,sqrt
from pylab import plot,show
from pylab import imshow,show,axis,contour,axis, figure,gray,hist,ion
"""
    refer to http://glowingpython.blogspot.com/2012/04/k-nearest-neighbor-search.html
"""

def knn_search(x, D, K):
    """ find K nearest neighbours of data among D """
    data_len = D.shape[0]
    K = K if K < data_len else data_len
    # euclidean distances from the other points
    sqd = sqrt(((D - x)**2).sum(axis=1))
    idx = argsort(sqd) # sorting
    # return the indexes of K nearest neighbours
    return idx[:K]

if __name__=='__main__':
    # knn_search test
    data = random.rand(200,2) # random dataset. everay point has 2 dimensions.
    x = random.rand(1,2) # query point.  

    # performing the search
    neig_idx = knn_search(x,data,10)

    # plotting the data and the input point
    plot(data[:,0],data[:,1],'ob',x[0,0],x[0,1],'or')
    # highlighting the neighbours
    plot(data[neig_idx,0],data[neig_idx,1],'o',
    markerfacecolor='None',markersize=15,markeredgewidth=1)
    show()

