# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from functools import wraps

def session_post_func(func, *args, **kwargs):
    return func(*args, **kwargs)


def client_run_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)


def client_tool_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def assistent_tool_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def assistant_run_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def assistant_stream_run_with_handler_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def assistent_stream_run_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def components_run_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def components_run_stream_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def list_trace_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def session_post(func):
    """
    对给定的函数添加 session post 请求装饰器
    
    Args:
        func (callable): 需要被装饰的函数
    
    Returns:
        callable: 返回一个装饰器函数，该函数在被调用时会使用 session post 请求执行原始函数
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return session_post_func(func, *args, **kwargs)
    
    return wrapper 


def client_run_trace(func):
    """
    为一个函数添加追踪功能，记录函数调用的开始和结束时间，以及函数的输入参数和返回结果。
    
    Args:
        func (callable): 需要被追踪的函数。
    
    Returns:
        callable: 封装后的函数，该函数在被调用时会执行原函数，并添加追踪功能。
    
    """
    @wraps(func)
    
    def wrapper(*args, **kwargs):

        return client_run_trace_func(func, *args, **kwargs)
    
    return wrapper 


def client_tool_trace(func):
    """
    装饰器函数，用于跟踪客户端工具函数的调用情况。
    
    Args:
        func (callable): 需要被跟踪的函数。
    
    Returns:
        callable: 返回一个装饰器函数，该函数会调用原函数并记录相关信息。
    
    """
    @wraps(func)

    def wrapper(*args, **kwargs):
        return client_tool_trace_func(func, *args, **kwargs)
    
    return wrapper 


def assistent_tool_trace(func):
    """
    用于辅助追踪函数执行情况的装饰器。
    
    Args:
        func (Callable[..., Any]): 需要被装饰的函数，接受任意数量和类型的参数。
    
    Returns:
        Callable[..., Any]: 返回一个函数，该函数会在调用原函数前后记录一些信息，
        然后将原函数的返回值返回。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistent_tool_trace_func(func, *args, **kwargs)
    
    return wrapper


def assistant_run_trace(func):
    """
    对函数进行装饰，用于在函数执行前后进行日志跟踪。
    
    Args:
        func (Callable): 需要进行日志跟踪的函数。
    
    Returns:
        Callable: 经过装饰后，带有日志跟踪功能的函数。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistant_run_trace_func(func, *args, **kwargs)
    
    return wrapper 

def assistent_stream_run_trace(func):
    """
    对目标函数进行包装，以启用辅助流执行追踪功能。
    
    Args:
        func (Callable): 需要包装的目标函数，必须是一个可调用的对象。
    
    Returns:
        Callable: 包装后的函数对象，调用时将执行辅助流执行追踪，并返回目标函数的执行结果。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistent_stream_run_trace_func(func, *args, **kwargs)
    
    return wrapper 

def assistent_stream_run_with_handler_trace(func):
    """
    为函数添加助手流运行和处理器跟踪的装饰器。
    
    Args:
        func (Callable): 需要被装饰的函数，即助手流运行的入口函数。
    
    Returns:
        Callable: 返回一个包装后的函数，该函数在调用时会执行assistant_stream_run_with_handler_trace_func函数，
                   并将原始函数func及其参数传递给它。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistant_stream_run_with_handler_trace_func(func, *args, **kwargs)
    
    return wrapper 

def components_run_trace(func):
    """
    为函数添加组件运行跟踪的装饰器。
    
    Args:
        func (Callable[..., Any]): 需要添加跟踪的函数。
    
    Returns:
        Callable[..., Any]: 装饰后的函数，当被调用时，会调用 components_run_trace_func 并传入原始函数和参数。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return components_run_trace_func(func, *args, **kwargs)
    
    return wrapper 

def components_run_stream_trace(func):
    """
    为给定的函数添加流追踪功能，用于追踪函数内部组件的运行情况。
    
    Args:
        func (callable): 需要添加流追踪功能的函数。
    
    Returns:
        callable: 返回一个装饰器函数，当被装饰的函数被调用时，会执行流追踪功能。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return components_run_stream_trace_func(func, *args, **kwargs)
    
    return wrapper

def list_trace(func):
    """
    为函数添加列表追踪的装饰器。
    
    Args:
        func (Callable[..., Any]): 需要被装饰的函数，接受任意数量和类型的参数。
    Returns:
        Callable[..., Any]: 返回一个装饰器函数，该函数在被调用时会执行原始函数并记录相关信息。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return list_trace_func(func, *args, **kwargs)
    
    return wrapper

