from time import time
from functools import cache
import ast
import inspect
import textwrap
from logging_decorator import log_dec

def timer(func):
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        print(f'Execution time {end - start:.7f}\n')
    return wrapper

@timer
def print_n_from_generator(gen, n, extra_line=False):
    res = ' '.join(str(next(gen)) for _ in range(n))
    print(f'\n{res}' if extra_line else res)

@log_dec()
def make_generator(function):
    arg = 1
    def generator(arg):
        while True:
            yield function(arg)
            arg += 1
    return generator(arg)

def _make_self_recursive(func):
    # Access the source code, deleting leading whitespace and parsing to an abstract syntax tree
    source_code = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source_code)

    func_name = func.__name__

    class RewriteCalls(ast.NodeTransformer):
        # Function called on every function node
        def visit_Call(self, node):
            # Recursively, visit all children nodes
            self.generic_visit(node)
            # Check if the called function is a direct call to the same function by name
            if isinstance(node.func, ast.Name) and node.func.id == func_name:
                # Change recursive call name: func(x) -> self(x)
                return ast.Call(func=ast.Name(id='self', ctx=ast.Load()),
                                args=node.args,
                                keywords=node.keywords)
            return node

    tree = RewriteCalls().visit(tree)
    # Recalculate lineno (line num of code node starts on), col_offset (num of characters)  
    ast.fix_missing_locations(tree)

    # Accessour changed function - first node
    func_def = tree.body[0]
    # Add the self argument [func(x) -> func(self, x)]
    func_def.args.args.insert(0, ast.arg(
        arg='self',
        lineno=func_def.lineno,
        col_offset=func_def.col_offset
    ))

    # Compile new function
    compiled = compile(ast.Module(body=[func_def], type_ignores=[]),
                       filename="<ast>", mode="exec")

    scope = {}
    # Run new fun, pass global variables, so that references still work, scope for storing local definitions
    exec(compiled, func.__globals__, scope)
    return scope[func.__name__]

def make_gen_mem(f):
    recursive_f = _make_self_recursive(f) # f(x) -> f(self, x), recursive calls: self(x)
    @cache
    def memoized(n):
        return recursive_f(memoized, n)
    return make_generator(memoized)

def fib_tail(n):
    def fib(n, a=0, b=1):
        if n == 0: return a
        return fib(n - 1, b, a + b)
    return fib(n)

def fib_rec(n):
    print(n, end=' ')
    if n == 0: return 0
    elif n == 1: return 1
    return fib_rec(n-1) + fib_rec(n-2)
    

sq_generator = make_generator(lambda x: x**2)
print('Squares:')
print_n_from_generator(sq_generator, 10)

aryth_generator = make_generator(lambda n: 1 + (n - 1) * 3)
print('Arithmetic sequence:')
print_n_from_generator(aryth_generator, 10)

geom_generator = make_generator(lambda n: -5 + 2**n)
print('Geometric sequence:')
print_n_from_generator(geom_generator, 10)


fib_generator = make_generator(fib_tail)
print('Fibonacci:')
print_n_from_generator(fib_generator, 20)

fib2_generator = make_generator(fib_rec)
print('Rec fibbonaci:')
print_n_from_generator(fib2_generator, 10, True)

fib3_generator = make_gen_mem(fib_rec)
print('Rec fibbonaci - cached generator:')
print_n_from_generator(fib3_generator, 10, True)

print('Rec fibbonaci - cached generator:')
print_n_from_generator(fib3_generator, 10, True)
