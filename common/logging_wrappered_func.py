
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(stdout_handler)

# def trace_log(logger=app.logger, lvl=logging.DEBUG):
#     def wrapper(func):
#         def wrappered_func(*args, **kwargs):
#             func_name = getattr(func, '__name__')
#             logger.log(lvl, '[{func_name}] enter'.format(func_name=func_name))
#             res = func(*args, **kwargs)
#             logger.log(lvl, '[{func_name}] exit'.format(func_name=func_name))
#             return res
#         return wrappered_func
#     return wrapper


