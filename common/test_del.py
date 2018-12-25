class B(object):
    def __init__(self):
        print "B init"

    def __del__(self):
        print "B del"
b = B()

