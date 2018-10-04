import os
import sys
from core import Graph
from pprint import pprint
# refer to https://github.com/cedricleroy/pyungo


if __name__ == '__main__':
    graph = Graph()

    @graph.register(inputs=['a', 'b'], outputs=['c'])
    def f_my_function(a, b):
        return a + b

#@graph.register(inputs=['d', 'a', {'x':100}, {'y':10}], outputs=['e'])
    def f_my_function3(d, a, x, y):
        print(y)
        return d - a + x

    graph.add_node(f_my_function3, inputs=['d', 'a', {'x':100}, {'y':10}], outputs=['e'])

    @graph.register(inputs=['c'], outputs=['d'])
    def f_my_function2(c):
        return c / 10.

    res = graph.calculate(data={'a': 2, 'b': 3})
    print(res)
