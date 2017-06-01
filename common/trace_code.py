import sys

# references:
# http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html
# https://docs.python.org/2/library/inspect.html

def h(x):
    return x+1

def f(x):
    x = h(x)
    return x+2

def g(x, a=1):
    print 'in g'
    print 'init x:', x
    t = x+a
    x = t
    print 'after x:', x
    return t

def main():
    """
    print "In main"
    for i in range(5):
        print i, i*3
    print "Done."
    """
    x = 0
    s = 1.0
    y1 = g(f(g(x, 4)), 6)
    y2 = g(f(f(y1)))
    y3 = h(y2)

"""
print main
print __file__
"""
def traceit(frame, event, arg):
    #print event
    if event == "line":
        lineno = frame.f_lineno
        #print "line", lineno
    elif event == 'call' and frame.f_back and frame.f_back.f_code.co_name == 'main' and frame.f_back.f_code.co_filename == __file__:
        print '======'
        print frame.f_locals
        print frame.f_code.co_varnames
        for var in frame.f_code.co_varnames:
            if var in frame.f_locals:
                print var, '->', frame.f_locals[var]
        print frame.f_back.f_code.co_name
        print event,frame.f_code.co_name, frame.f_code, frame, frame.f_back
    return traceit


sys.settrace(traceit)
main()
