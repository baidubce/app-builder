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
import os
import sys
import traceback
import _testcapi
from functools import wraps

def _whether_enable_trace():
    if os.environ.get('ENABLE_SENTRY_TRACE', None) == 'true' and os.environ.get('SENTRY_DSN', None):
        return True
    elif os.environ.get('APPBUILDER_SDK_TRACE_ENABLE', None) == 'true':
        return True
    else:
        return False

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
    将指定的函数装饰为使用 session_post_func 发送 POST 请求的函数。
    
    Args:
        func (Callable): 被装饰的函数。
    
    Returns:
        Callable: 返回一个新的函数，该函数会在被调用时通过 session_post_func 发送 POST 请求。
    
    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():  
            try:
                return session_post_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
                
    return wrapper 


def client_run_trace(func):
    """
    对传入的函数进行装饰，添加客户端运行跟踪功能。
    
    Args:
        func (callable): 需要被装饰的函数。
    
    Returns:
        callable: 返回一个包装后的函数，该函数在执行时会调用 client_run_trace_func 函数，
                  并传入原始函数及其参数。
    
    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return client_run_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise

    return wrapper 


def client_tool_trace(func):
    """
    装饰器函数，用于跟踪客户端工具函数的调用情况。
    
    Args:
        func (callable): 需要被跟踪的函数。
    
    Returns:
        callable: 返回一个装饰器函数，该函数会调用原函数并记录相关信息。
    
    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return client_tool_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
    return wrapper 


def assistent_tool_trace(func):
    """
    用于辅助追踪函数执行情况的装饰器。
    
    Args:
        func (Callable[..., Any]): 需要被装饰的函数，接受任意数量和类型的参数。
    
    Returns:
        Callable[..., Any]: 返回一个函数，该函数会在调用原函数前后记录一些信息，
        然后将原函数的返回值返回。
    
    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return assistent_tool_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
    
    return wrapper


def assistant_run_trace(func):
    """
    对函数进行装饰，用于在函数执行前后进行日志跟踪。
    
    Args:
        func (Callable): 需要进行日志跟踪的函数。
    
    Returns:
        Callable: 经过装饰后，带有日志跟踪功能的函数。

    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return assistant_run_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
    
    return wrapper 

def assistent_stream_run_trace(func):
    """
    对目标函数进行包装，以启用辅助流执行追踪功能。
    
    Args:
        func (Callable): 需要包装的目标函数，必须是一个可调用的对象。
    
    Returns:
        Callable: 包装后的函数对象，调用时将执行辅助流执行追踪，并返回目标函数的执行结果。

    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return assistent_stream_run_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
        
    return wrapper 

def assistent_stream_run_with_handler_trace(func):
    """
    为函数添加助手流运行和处理器跟踪的装饰器。
    
    Args:
        func (Callable): 需要被装饰的函数，即助手流运行的入口函数。
    
    Returns:
        Callable: 返回一个包装后的函数，该函数在调用时会执行assistant_stream_run_with_handler_trace_func函数，
                   并将原始函数func及其参数传递给它。

    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return assistant_stream_run_with_handler_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
    
    return wrapper 

def components_run_trace(func):
    """
    为函数添加组件运行跟踪的装饰器。
    
    Args:
        func (Callable[..., Any]): 需要添加跟踪的函数。
    
    Returns:
        Callable[..., Any]: 装饰后的函数，当被调用时，会调用 components_run_trace_func 并传入原始函数和参数。

    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():    
            try:
                return components_run_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
                
    return wrapper

def components_run_stream_trace(func):
    """
    为给定的函数添加流追踪功能，用于追踪函数内部组件的运行情况。
    
    Args:
        func (callable): 需要添加流追踪功能的函数。
    
    Returns:
        callable: 返回一个装饰器函数，当被装饰的函数被调用时，会执行流追踪功能。

    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return components_run_stream_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
  
    
    return wrapper

def list_trace(func):
    """
    为函数添加列表追踪的装饰器。
    
    Args:
        func (Callable[..., Any]): 需要被装饰的函数，接受任意数量和类型的参数。

    Returns:
        Callable[..., Any]: 返回一个装饰器函数，该函数在被调用时会执行原始函数并记录相关信息。
    
    Raises:
        Exception: 如果在发送 POST 请求时发生异常，并且环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则直接抛出异常；
                  否则，尝试捕获异常并生成自定义的异常信息后抛出。
    
    Note:
        如果环境变量 APPBUILDER_TRACE_DEBUG 被设置为 "true"，则在发生异常时将直接抛出原始异常。
        否则，会尝试过滤掉与 "appbuilder/utils/trace" 相关的堆栈跟踪，并生成自定义的异常信息后抛出。
        如果在生成自定义异常信息的过程中发生异常，则会直接抛出原始异常。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _whether_enable_trace():
            try:
                return list_trace_func(func, *args, **kwargs)
            except Exception as e:
                if os.getenv("APPBUILDER_TRACE_DEBUG", "None").lower() == "true":
                    raise
                else:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filtered_tb = [frame for frame in tb if "appbuilder/utils/trace" not in frame.filename]
                    formatted_lines = traceback.format_list(filtered_tb)
                    formatted_lines += traceback.format_exception_only(exc_type, exc_value)
                    custom_traceback = ''.join(formatted_lines)
                    exception_type = type(e)
                    try:
                        try:
                            exception_type('\n'+custom_traceback)
                        except Exception:
                            raise e from None
                        raise exception_type('\n'+custom_traceback) from None
                    except:
                        tp, exc, tb = sys.exc_info()
                        _testcapi.set_exc_info(tp, exc, tb.tb_next)
                        del tp, exc, tb
                        raise
        else:
            try:
                return func(*args, **kwargs)
            except:
                tp, exc, tb = sys.exc_info()
                _testcapi.set_exc_info(tp, exc, tb.tb_next)
                del tp, exc, tb
                raise
    
    return wrapper

