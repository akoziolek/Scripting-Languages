import sys
import logging
import logger #...
import inspect
from time import perf_counter
from functools import wraps

logger = logging.getLogger(__name__)

def log(level=logging.DEBUG):
    def decorator(instance):
        if isinstance(instance, type):
            old_init = instance.__init__
            
            @wraps(instance)
            def new__init__(self, *args, **kwargs):
                logger.log(level, f'Start of object {instance.__name__} initialization')
                old_init(self, *args, **kwargs)
                logger.log(level, f'End of object {instance.__name__} initialization')


            instance.__init__ = new__init__
            return instance
            
        elif callable(instance):
            @wraps(instance)
            def wrapper(*args, **kwargs):
                logger.log(level, f'Function {instance.__name__} has been called.')
                
                args_names = inspect.getfullargspec(instance)[0]
                args_dict = dict(zip(args_names, args))
                logger.log(level, f'Arguments passed {args_dict | kwargs}')
                
                start = perf_counter()
                result = instance(*args, **kwargs)
                end = perf_counter()
                logger.log(level, f'Elapsed time: {end-start:.8f}')
                logger.log(level, f'Result of {instance.__name__}: {result}')
            return wrapper
    return decorator

@log()
def fun1(a, b, c, d):
    return a + b + c
fun1(1, 2, 3, d=0)

@log()
class sth:
    def __init__(self, a):
        self.a = a

sth(2)


# logger for generator

""" def function_call(*args, **kwargs):
                log_fun(f"Function call - {param.__name__}")
                if args:
                    log_fun(f"Positional args: {args}")
                if kwargs:
                    log_fun(f"Keyword args: {kwargs}")
                start = time.perf_counter()
                result = param(*args, **kwargs)
                end = time.perf_counter()
                log_fun(f"Result: {result}")
                log_fun(f"Execution time: {((end - start) * 1000):.3f} ms")
                return result
            return function_call
        
        elif inspect.isclass(param):
            original_init = param.__init__
            @wraps(param)
            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                log_fun(f"Class {param.__name__} initialized!")
            param.__init__ = new_init
            return param """