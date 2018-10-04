def foo():
    if foo.counter is None:
        foo.counter = 0
    foo.counter += 1
    print "Counter is %d" % foo.counter
foo.counter = None

foo()
foo()
foo()
foo()
