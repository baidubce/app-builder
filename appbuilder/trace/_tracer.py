from functools import wraps


def run_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)


def tool_eval_streaming_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)


def assistant_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)


def run_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        return run_trace_func(func, *args, **kwargs)
        
    return wrapper


def tool_eval_streaming_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        return tool_eval_streaming_trace_func(func, *args, **kwargs)
        
    return wrapper


def assistant_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        return assistant_trace_func(func, *args, **kwargs)
    
    return wrapper