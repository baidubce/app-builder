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

def session_post(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return session_post_func(func, *args, **kwargs)
    
    return wrapper 


def client_run_trace(func):
    @wraps(func)
    
    def wrapper(*args, **kwargs):

        return client_run_trace_func(func, *args, **kwargs)
    
    return wrapper 


def client_tool_trace(func):
    @wraps(func)

    def wrapper(*args, **kwargs):
        return client_tool_trace_func(func, *args, **kwargs)
    
    return wrapper 


def assistent_tool_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistent_tool_trace_func(func, *args, **kwargs)
    
    return wrapper


def assistant_run_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistant_run_trace_func(func, *args, **kwargs)
    
    return wrapper 

def assistent_stream_run_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistent_stream_run_trace_func(func, *args, **kwargs)
    
    return wrapper 

def assistent_stream_run_with_handler_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return assistant_stream_run_with_handler_trace_func(func, *args, **kwargs)
    
    return wrapper 

def components_run_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return components_run_trace_func(func, *args, **kwargs)
    
    return wrapper 

def components_run_stream_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return components_run_stream_trace_func(func, *args, **kwargs)
    
    return wrapper

