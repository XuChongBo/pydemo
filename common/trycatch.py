def get_decorator(errors=(Exception, ), default_value=''):
    def decorator(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors, e:
                print "Got error! ", repr(e)
                return default_value
        return new_func
    return decorator

try_except = get_decorator(default_value='default')
a = {}

@try_except
def example1(a):
    return a['b']

@try_except
def example2(a):
    return doesnt_exist()

print example1(a)
print example2(a)
