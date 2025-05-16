import sys
import logging
import Lab7.logger_config as logger_config
import inspect
from time import perf_counter
from functools import wraps

logger_config = logging.getLogger(__name__)

def log_dec(level=logging.DEBUG):
    def decorator(instance):
        if isinstance(instance, type):
            old_init = instance.__init__
            
            @wraps(instance)
            def new__init__(self, *args, **kwargs):
                logger_config.log(level, f'Start of object {instance.__name__} initialization')
                old_init(self, *args, **kwargs)
                logger_config.log(level, f'End of object {instance.__name__} initialization')

            instance.__init__ = new__init__
            return instance
            
        elif callable(instance):
            @wraps(instance)
            def wrapper(*args, **kwargs):
                logger_config.log(level, f'Function {instance.__name__} has been called.')
                
                args_names = inspect.getfullargspec(instance)[0]
                args_dict = dict(zip(args_names, args))
                logger_config.log(level, f'Arguments passed {args_dict | kwargs}')
                
                start = perf_counter()
                result = instance(*args, **kwargs)
                end = perf_counter()
                logger_config.log(level, f'Elapsed time: {end-start:.8f}')
                logger_config.log(level, f'Result of {instance.__name__}: {result}')
                return result
            return wrapper
    return decorator

@log_dec()
def fun1(a, b, c, d):
    return a + b + c
fun1(1, 2, 3, d=0)

@log_dec()
class dog:
    def __init__(self, name):
        self.name = name

dog1 = dog('Julek')
