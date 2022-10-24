import timeit
from functools import wraps


def benchmark(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        starting = timeit.default_timer()
        f = function(*args, **kwargs)
        ending = timeit.default_timer() - starting
        print(f"El proceso demoro: {ending} segundos")
        return f
    
    
    return decorator
