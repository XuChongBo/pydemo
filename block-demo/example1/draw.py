from graphviz import Digraph
from torch.autograd import Variable
import torch
import torchvision


def make_dot(var):
    node_attr = dict(style='filled',
                     shape='box',
                     align='left',
                     fontsize='12',
                     ranksep='0.1',
                     height='0.2')
    dot = Digraph(node_attr=node_attr, graph_attr=dict(size="12,12"))
    seen = set()

    def add_nodes(var):
        if var not in seen:
            print str(type(var).__name__)
            if isinstance(var, Variable):
                value = '('+(', ').join(['%d'% v for v in var.size()])+')'
                dot.node(str(id(var)), str(value), fillcolor='lightblue')
                print value
            else:
                dot.node(str(id(var)), str(type(var).__name__))
            seen.add(var)
            if hasattr(var, 'previous_functions'):
                for u in var.previous_functions:
                    dot.edge(str(id(u[0])), str(id(var)))
                    add_nodes(u[0])
    add_nodes(var.creator)
    return dot

if __name__ == "__main__":
    vggnet19 = torchvision.models.vgg19()
    import torch.nn as nn
    vggnet19.classifier = nn.Linear(8192,4096)
    inputs = torch.randn(1,3,128,128)
    y = vggnet19(Variable(inputs))
    net_view = make_dot(y)
#net_view.view()


