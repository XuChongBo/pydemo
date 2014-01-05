#!/usr/bin/env python

import cPickle
import gzip
import time
import PIL.Image

import numpy
import theano
import theano.tensor as T
import os

from theano.tensor.shared_randomstreams import RandomStreams
#from utils import tile_raster_images

working_path='/Users/xcbfreedom/projects/'
os.chdir(working_path)

def shared_dataset(data_xy, borrow=True):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """
    data_x, data_y = data_xy
    shared_x = theano.shared(numpy.asarray(data_x,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    shared_y = theano.shared(numpy.asarray(data_y,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x, T.cast(shared_y, 'int32')


def load_mnist_data(dataset):
    ''' Loads the dataset
    :type dataset: string
    :param dataset: the path to the dataset (here MNIST)
    '''
    #############
    # LOAD DATA #
    #############

    f = gzip.open(dataset, 'rb')
    train_set, valid_set, test_set = cPickle.load(f)
    f.close()
    #train_set, valid_set, test_set format: tuple(input, target)
    #input is an numpy.ndarray of 2 dimensions (a matrix)
    #witch row's correspond to an example. target is a
    #numpy.ndarray of 1 dimensions (vector)) that have the same length as
    #the number of rows in the input. It should give the target
    #target to the example with the same index in the input.

    test_set_x, test_set_y = shared_dataset(test_set)
    valid_set_x, valid_set_y = shared_dataset(valid_set)
    train_set_x, train_set_y = shared_dataset(train_set)

    rval = [(train_set_x, train_set_y), 
            (valid_set_x, valid_set_y),
            (test_set_x, test_set_y)]
    return rval


def show_mnist_data():
    datasets = load_mnist_data('./data/mnist.pkl.gz')
    train_set_x, train_set_y = datasets[0]
    valid_set_x, valid_set_y = datasets[1]
    test_set_x, test_set_y = datasets[2]
    #train_set_x.get_value(borrow=True).shape[0] 
    print type(train_set_x[0][0]),type(train_set_y[0]),train_set_y[0].eval()
    print train_set_y[0]
    print train_set_x.type, train_set_y.type
    #x=T.matrix()
    #print type(x),x.eval()
    print train_set_x.get_value(borrow=True).shape 
    #print train_set_y.get_value(borrow=True).shape 
    print type(train_set_y.evaluate({}))
    print train_set_x[0][0]

    # Construct image from the weight matrix
    """
    image = PIL.Image.fromarray(tile_raster_images(
             X=rbm.W.get_value(borrow=True).T,
             img_shape=(28, 28), tile_shape=(10, 10),
             tile_spacing=(1, 1)))
    #image.save('filters_at_epoch_%i.png' % epoch)
    """

if __name__ == '__main__':
    show_mnist_data()
