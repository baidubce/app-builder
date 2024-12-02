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
import time
import json
import inspect
from opentelemetry import trace
from pydantic import BaseModel
from appbuilder import Message

from appbuilder import AppbuilderTraceException
from appbuilder.core.component import ComponentOutput

import logging
logging.basicConfig(level=logging.INFO)

def _time(start_time,end_time,span):
    """
    设置时间跨度属性为两个时间点的差值（秒）。
    
    Args:
        start_time (float): 开始时间的时间戳（秒为单位）。
        end_time (float): 结束时间的时间戳（秒为单位）。
        span (object): OpenTelemetry的Span对象，用于设置时间跨度属性。
    
    Returns:
        None: 该函数不返回任何值，直接在传入的span对象上设置属性。
    
    """
    span.set_attribute('time.cost-time',str(end_time-start_time)+'s')

def _build_curl_from_post(url, headers, json_body, timeout) -> str:
        """
        从 POST 请求参数生成 cURL 命令。
        
        Args:
            url (str): 请求的 URL 地址。
            headers (dict): 请求头信息，以字典形式传入。
            json_body (dict): JSON 格式的请求体数据，以字典形式传入。
            timeout (int, optional): 请求的超时时间（秒）。默认为 None，表示不设置超时时间。
        
        Returns:
            str: 生成的 cURL 命令字符串。
        
        """
        curl = f"curl -L '{url}' \\\n"
        header_lines = [f"-H '{k}: {v}' \\" for k, v in headers.items() if k != 'Content-Length']
        if header_lines:
            header_lines[-1] = header_lines[-1].rstrip(" \\")
        curl += "\n".join(header_lines)
        
        if json_body:
            body = f"'{json.dumps(json_body, ensure_ascii=False)}'"
            curl += f" \\\n-d {body}"
        
        if timeout is not None:
            curl += f" \\\n--max-time {timeout}"
            
        return curl


def _post_input(args,kwargs,span):
    """
    使用 POST 请求发送数据并记录相关属性到 span 中。
    
    Args:
        args (tuple): 元组，其中最后一个元素是发送 POST 请求的 URL。
        kwargs (dict): 字典，包含以下可选参数：
            - headers (dict): HTTP 请求头，以字典形式表示。
            - json (dict, optional): 发送的 JSON 数据体，默认为 None。
            - timeout (int, optional): 请求超时时间（秒），默认为 None。
        span (object): OpenTelemetry 的 span 对象，用于记录相关属性。
    
    Returns:
        None: 该函数没有返回值，主要用于发送 POST 请求并记录相关信息。
    
    """
    url = kwargs.get('url',None)
    if not url:        
        url = args[-1]
    curl=_build_curl_from_post(
        url=url, 
        headers=kwargs['headers'], 
        json_body=kwargs.get('json',None), 
        timeout=kwargs.get('timeout',None), 
        )
    span.set_attribute("input.value","{}".format(curl))


def _input(args,kwargs,span):
    """
    将函数参数转化为字符串形式并存储在字典中，然后将字典转化为JSON字符串并设置为span的属性。
    
    Args:
        args (tuple): 函数的位置参数元组。
        kwargs (dict): 函数的关键字参数字典。
        span (opentracing.Span): 用于记录日志的OpenTracing span对象。
    
    Returns:
        None: 此函数没有返回值，主要用于设置span的属性。
    
    Raises:
        无特定异常抛出，但如果在处理参数或设置span属性时发生异常，将打印异常信息。
    
    """
    input_dict={}
    type_name = (bool,str,bytes,int,float,list,dict)
    sig = inspect.signature(args[0])
    params = sig.parameters
    try:
        if args:
            for idx, value in enumerate(list(args)):
                if isinstance(value, type_name):
                    input_dict[list(params)[idx-1]] = str(value)
                elif isinstance(value, Message):
                    input_dict[list(params)[idx-1]] = str(value)
            for key, value in dict(kwargs).items():
                if isinstance(value, type_name):
                    input_dict[key] = value
                elif isinstance(value, Message):
                    input_dict[key] = str(value)
        if input_dict:
            if os.environ.get('OPENINFERENCE_TRACE','true') == 'true' and os.environ.get('SENTRY_DSN', None):
                span.set_data("input-value",json.dumps(input_dict, ensure_ascii=False))
            else:
                span.set_attribute("input.value",json.dumps(input_dict, ensure_ascii=False))
    except Exception as e:
        raise AppbuilderTraceException(e)

def _client_tool_trace_output_deep_iterate(output,span):
    """
    对输出进行深度遍历，并将结果以JSON格式记录到span的属性中
    
    Args:
        output (dict, bool, str, bytes, int, float, list): 需要遍历的输出对象
        span (Span): 用于记录输出结果的span对象
    
    Returns:
        None
    
    """
    input_dict={}
    type_name = (bool,str,bytes,int,float,list)
   
    if isinstance(output, dict):
        for key, value in output.items():
            if isinstance(value, type_name):
                input_dict[key] = str(value)
        span.set_attribute("output.value",json.dumps(input_dict, ensure_ascii=False))
    else:
        if isinstance(output, type_name):
            span.set_attribute("output.value",str(output))

def _client_trace_generator(generator, tracer, parent_context):
    """
    用于生成客户端跟踪信息的生成器函数。
    
    Args:
        generator (Iterator): 消息生成器。
        tracer (Tracer): OpenTelemetry 追踪器实例。
        parent_context (SpanContext): 父级上下文。
    
    Returns:
        Generator: 带有跟踪信息的消息生成器。
    
    """
    with tracer.start_as_current_span('AppBuilderClient-Stream-RUN', context = parent_context) as span:
        span.set_attribute("openinference.span.kind", 'agent')
        result_str = ''
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        run_list = []
        try:
            new_span = tracer.start_span('Client-Stream')
            for message in generator:
                new_span.set_attribute("openinference.span.kind", 'agent')
                context_message_str = ""
                has_reference = False

                context_message_list = None
                if hasattr(message, 'events') and message.events and hasattr(message.events[0], 'detail') and message.events[0].detail:
                    context_message_list = message.events[0].detail.get('references', None)

                if context_message_list:
                    for context_message in context_message_list:
                        for context_message_key, context_message_value in context_message.items():
                            context_message_str += '{}: {}\n'.format(context_message_key, context_message_value)
                            has_reference = True
                        context_message_str += '\n'

                if has_reference:
                    new_span.set_attribute("input.value", 'Context(上下文) For RAG:\n{}'.format(context_message_str))

                new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))

                result_str += str(message.answer)

                if hasattr(message, 'events') and message.events and hasattr(message.events[0], 'event_type') and hasattr(message.events[0], 'status'):
                    run_list.append('{}[status:{}]'.format(message.events[0].event_type, message.events[0].status))

                if hasattr(message, 'events') and message.events and hasattr(message.events[0], 'usage') and message.events[0].usage:
                    prompt_tokens = message.events[0].usage.prompt_tokens
                    completion_tokens = message.events[0].usage.completion_tokens
                    total_tokens = message.events[0].usage.total_tokens
                new_span.end()
                new_span = tracer.start_span('Client-Stream')
                yield message
        except Exception as e:
            raise AppbuilderTraceException(str(e))  
        finally:
            span.set_attribute("output.value", result_str)
            span.set_attribute("llm.token_count.prompt", prompt_tokens)
            span.set_attribute("llm.token_count.completion", completion_tokens)
            span.set_attribute("llm.token_count.total", total_tokens)
            span.set_attribute("Agent-Running-Process", '==>'.join(run_list))
        
        
def _client_run_trace_stream(tracer, func, *args, **kwargs):
    """
    跟踪客户端运行流处理函数，并记录相关的跟踪信息。
    
    Args:
        tracer (Tracer): OpenTelemetry Tracer 实例，用于生成和设置 span。
        func (Callable[..., Any]): 客户端运行的函数，通常是一个返回流处理结果的函数。
        *args: 可变位置参数，传递给 func 的参数。
        **kwargs: 可变关键字参数，传递给 func 的参数。
    
    Returns:
        Any: 函数的返回值，通常是一个包含流处理结果的响应对象。
    
    """
    with tracer.start_as_current_span('AppBuilderClient-Stream-RUN', context=None) as parent_span:
        parent_context = trace.set_span_in_context(parent_span)
        parent_span.set_attribute("openinference.span.kind", 'Agent')
        start_time = time.time()
        result = func(*args, **kwargs)
        
        _input(args=args, kwargs=kwargs, span=parent_span)
        
        generator = result.content
        result.content = _client_trace_generator(generator=generator, tracer=tracer, parent_context=parent_context)
        
        end_time = time.time()
        _time(start_time=start_time, end_time=end_time, span=parent_span)
    return result

def _client_run_trace_un_stream(tracer, func, *args, **kwargs):
    """
    执行函数func，并追踪其运行过程，同时记录相关性能指标和事件信息。
    
    Args:
        tracer (Any): 追踪器对象，用于开始、结束和设置span属性。
        func (Callable[..., Any]): 要执行的函数。
        *args: 可变位置参数，传递给func的参数。
        **kwargs: 可变关键字参数，传递给func的参数。
    
    Returns:
        Any: 函数func的返回值。
    
    """
    with tracer.start_as_current_span('AppBuilderClient-RUN') as span:
        start_time = time.time()
        result = func(*args, **kwargs)
        span.set_attribute("openinference.span.kind", 'Agent')
        _input(args=args, kwargs=kwargs, span=span)
        run_list = []
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        span.set_attribute("output.value", result.content.answer)
        events = result.content.events
        for event in events:
            run_list.append('{}[status:{}]'.format(event.event_type, event.status))
            if hasattr(event, 'usage') and event.usage and hasattr(event.usage, 'prompt_tokens'):
                prompt_tokens = event.usage.prompt_tokens
                completion_tokens = event.usage.completion_tokens
                total_tokens = event.usage.total_tokens

        if total_tokens:
            span.set_attribute("llm.token_count.prompt", prompt_tokens)
            span.set_attribute("llm.token_count.completion", completion_tokens)
            span.set_attribute("llm.token_count.total", total_tokens)
        span.set_attribute("Agent-Running-Process", '==>'.join(run_list))

        end_time = time.time()
        _time(start_time=start_time, end_time=end_time, span=span)

        return result



def _output(output, span):
    """
    将输出值转换为字符串并设置到span的属性中
    
    Args:
        output (Any): 待输出的值，可以是任意类型，但如果是BaseModel或其子类或类对象，将使用model_dump_json方法进行序列化
        span (Span): Jaeger的Span对象，用于记录跟踪信息
    
    Returns:
        None: 此函数不返回任何值，但会将输出值转换为字符串并设置到span的属性中
    
    Raises:
        无: 此函数不引发任何异常
    
    """
    type_name = (bool,str,bytes,int,float,list,dict)
    if isinstance(output, BaseModel) or inspect.isclass(output):
        span.set_attribute("output.value", "{}".format(output.model_dump_json(indent=4)))
    elif isinstance(output, type_name):
        _client_tool_trace_output_deep_iterate(output=output,span=span)


def _tool_name(args):
    """
    根据传入的函数或方法对象，返回其工具名称。
    
    Args:
        args (tuple): 包含单个元素的元组，该元素为函数或方法对象。
    
    Returns:
        str: 返回字符串，表示函数或方法的工具名称。
    
            - 如果函数或方法是类的实例方法，则返回形如"类名-方法名"的字符串。
            - 如果函数或方法不是类的实例方法，则直接返回函数或方法名。
    
    """

    class_name = args[0].__qualname__.split('.')[0]
    function_name = args[0].__name__
    if class_name == function_name:
        return "{}".format(function_name) 
    else:
        return "{}-{}".format(class_name,function_name)
    

def _assistant_output(output, span):
    """
    设置span的属性，将output的模型转储为JSON格式的字符串并赋值给span的output.value属性。
    
    Args:
        output (Any): 任意类型的数据，预期是包含模型转储功能的对象。
        span (Span): 用于设置属性的span对象。
    
    Returns:
        None: 该函数不返回任何值，而是通过修改span对象来实现功能。
    
    """
    span.set_attribute("output.value", "{}".format(output.model_dump_json(indent=4)))

def _assistant_stream_run_with_handler_output(generator , tracer, parent_context):
    """
    执行带有处理函数输出的辅助流。
    
    Args:
        generator (Generator): 一个生成器，用于产生消息。
        tracer (Tracer): OpenTelemetry 追踪器实例。
        parent_context (Context): 父级上下文，用于追踪的上下文。
    
    Returns:
        Generator: 一个生成器，产生消息并可能包含额外的输出信息。
    
    """
    with tracer.start_as_current_span("Assistant-stream_run_with_handler", context=parent_context) as span:
        span.set_attribute("openinference.span.kind",'Agent')
        result = ''
        output_list = []
        try:
            new_span = tracer.start_span('Assistant-Stream_run_with_handler')
            for message in generator:
                new_span.set_attribute("openinference.span.kind",'agent')
                if isinstance(message, BaseModel):
                    new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))
                else:
                    new_span.set_attribute("output.value", "{}".format(json.dumps(message, ensure_ascii=False)))
                if hasattr(message, 'content') and message.content and message.content[0]:
                    if hasattr(message.content[0], 'text') and message.content[0].text:
                        if hasattr(message.content[0].text, 'value') and message.content[0].text.value: 
                            output_list.append(message.content[0].text.value)
                new_span.end()
                new_span = tracer.start_span('Assistant-Stream_run_with_handler')
                yield message
        except Exception as e:
            raise AppbuilderTraceException(str(e))
        finally:
            new_span.set_attribute("output.value",'流式运行结束')
            new_span.set_attribute("openinference.span.kind",'agent')   
            new_span.end()
            for item in output_list:
                result += str(item)
            span.set_attribute("output.value", result)

def _assistant_stream_output(output, span, tracer):
    """
    处理流式输出，并生成追踪信息。
    
    Args:
        output (Iterator[Any]): 流式输出数据的迭代器。
        span (Span): 追踪信息的Span对象。
        tracer (Tracer): 追踪信息的Tracer对象。
    
    Returns:
        List[Any]: 存储所有输出消息的列表。
    
    """
    result = ''
    run_list = []
    generator_list = []
    if output:
        new_span = tracer.start_span('Assistant-Stream_run')
        for message in output:
            generator_list.append(message)
            new_span.set_attribute("openinference.span.kind",'agent')
            if message.event == "status":
                new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))
            elif message.event == "message":
                new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))
                if hasattr(message, 'content') and message.content and hasattr(message.content[0], 'text') and message.content[0].text and hasattr(message.content[0].text, 'value'):
                    run_list.append(message.content[0].text.value)
            new_span.end()
            new_span = tracer.start_span('Assistant-Stream_run')
        for item in run_list:
            result += str(item) 
        new_span.set_attribute("output.value",'流式输出结束\n输出结果为:{}'.format(result))
        new_span.set_attribute("openinference.span.kind",'agent')
        new_span.end()
        span.set_attribute("output.value",result)
    return generator_list

def _components_run_output(output, span):
    """
    设置span的属性以记录输出信息。
    
    Args:
        output (Any): 运行组件后得到的输出对象，需要包含 `token_usage` 属性（如果存在）。
        span (Span): Jaeger中的span对象，用于记录追踪信息。
    
    Returns:
        None: 此函数不返回任何值，而是直接修改span对象的属性。
    
    """
    if hasattr(output, 'token_usage') and output.token_usage:
        span.set_attribute("llm.token_count.prompt", output.token_usage.get('prompt_tokens', 0))
        span.set_attribute("llm.token_count.completion", output.token_usage.get('completion_tokens', 0))
        span.set_attribute("llm.token_count.total", output.token_usage.get('total_tokens', 0)) 
    span.set_attribute("output.value", "{}".format(output.model_dump_json(indent=4)))    


def _post_trace(tracer, func, *args, **kwargs):
    """
    对指定的HTTP POST请求函数进行追踪，并生成追踪信息。
    
    Args:
        tracer (Any): 追踪器实例，用于开始和结束追踪。
        func (Callable[..., Any]): 需要被追踪的HTTP POST请求函数。
        *args: 可变位置参数，用于传递给func函数。
        **kwargs: 可变关键字参数，用于传递给func函数。
    
    Returns:
        Any: func函数的返回值。
    
    """
    url = args[-1]
    if not isinstance(url, str):
        url = kwargs.get('url','')
    method = url.split('/')[-1]
    with tracer.start_as_current_span("HTTP-POST: {}".format(method)) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        new_span.set_attribute("openinference.span.kind",'tool')
        _time(start_time = start_time,end_time = end_time,span = new_span)
        _post_input(args = args, kwargs = kwargs,span = new_span)
    return result

def _client_run_trace(tracer, func, *args, **kwargs):
    """
    在客户端运行跟踪函数，根据参数决定是否以流模式执行
    
    Args:
        tracer (Any): 跟踪器实例
        func (Callable): 需要跟踪的函数
        *args (tuple): 函数的可变位置参数
        **kwargs (dict): 函数的可变关键字参数
    
    Returns:
        Any: 跟踪函数的执行结果，根据stream参数的值，返回_client_run_trace_stream或_client_run_trace_un_stream的返回值
    
    Raises:
        无特定异常，但可能抛出在执行函数时发生的任何异常
    
    """
    sig = inspect.signature(args[0])
    params = sig.parameters
    stream = False
    if args:
        for idx, value in enumerate(list(args)):
            if list(params)[idx-1] == 'stream':
                stream = value
    if kwargs:
        for key, value in dict(kwargs).items():
            if key == 'stream':
                stream = value
    if stream:
        return _client_run_trace_stream(tracer, func, *args, **kwargs)
    if not stream:
        return _client_run_trace_un_stream(tracer, func, *args, **kwargs)

    
def _client_tool_trace(tracer, func, *args, **kwargs):
    """
    追踪客户端工具函数的调用，记录相关信息到追踪器。
    
    Args:
        tracer (Any): 追踪器实例，用于创建和记录追踪信息。
        func (Callable[..., Any]): 要追踪的客户端工具函数。
        *args (Any): 传递给func的位置参数。
        **kwargs (Any): 传递给func的关键字参数。
    
    Returns:
        Any: func函数执行后的返回值。
    
    """
    with tracer.start_as_current_span(_tool_name(args=args)) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'tool')
        _output(output=result, span = new_span)
    return result

def _assistant_tool_trace(tracer, func, *args, **kwargs):
    """
    对给定的函数进行追踪，记录其执行的时间、输入和输出。
    
    Args:
        tracer: OpenTelemetry的Tracer实例，用于创建span。
        func: 需要追踪的函数。
        *args: 传递给func的位置参数。
        **kwargs: 传递给func的关键字参数。
    
    Returns:
        func的返回值。
    
    """
    span_name = _tool_name(args=args)
    with tracer.start_as_current_span(span_name) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        _input(args = args, kwargs = kwargs, span=new_span)
        new_span.set_attribute("openinference.span.kind",'tool')
        if result:
            _output(output=result, span = new_span)
    return result

def _assistant_run_trace(tracer, func, *args, **kwargs):
    """
    使用给定的追踪器(tracer)对函数(func)的执行进行追踪。
    
    Args:
        tracer (object): 追踪器对象，用于创建和操作追踪的span。
        func (callable): 需要被追踪的函数。
        *args (tuple): 传递给func的位置参数。
        **kwargs (dict): 传递给func的关键字参数。
    
    Returns:
        Any: 被追踪函数func的返回值。
    
    """
    with tracer.start_as_current_span("Assistant-RUN") as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'Agent')
        _input(args = args, kwargs = kwargs, span=new_span)
        _assistant_output(output=result, span = new_span)
    return result

def _assistant_stream_trace(tracer, func, *args, **kwargs):
    """
    为辅助流跟踪的函数提供跟踪功能。
    
    Args:
        tracer (Tracer): OpenTelemetry 的 Tracer 实例，用于生成和操作跟踪数据。
        func (Callable): 需要进行流跟踪的函数。
        *args: 传递给 func 的位置参数。
        **kwargs: 传递给 func 的关键字参数。
    
    Returns:
        Generator[Any, None, None]: 一个生成器，生成 func 函数的执行结果。
    
    """
    with tracer.start_as_current_span("Assistant-stream_run") as span:
        start_time = time.time()
        result=func(*args, **kwargs)
        span.set_attribute("openinference.span.kind",'Agent')
        _input(args = args, kwargs = kwargs, span=span)
        run_list = []
        new_span = tracer.start_span("Assistant-stream_run")
        for message in result:
            new_span.set_attribute("openinference.span.kind",'agent')
            if message.event == "status":
                new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))
            elif message.event == "message":
                new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))
                if hasattr(message, 'content') and message.content and hasattr(message.content[0], 'text') and message.content[0].text and hasattr(message.content[0].text, 'value'):
                    run_list.append(message.content[0].text.value)
            new_span.end()
            new_span = tracer.start_span('Assistant-Stream_run')
            yield message
        end_time = time.time()  
        _time(start_time = start_time,end_time = end_time,span = span)
        result_str = ''.join(str(res) for res in run_list)
        span.set_attribute("output.value",result_str)


def _assistant_stream_run_with_handler_trace(tracer, func, *args, **kwargs):
    """
    在带有追踪器的上下文中运行函数，并捕获函数执行过程中的输入和输出，以及耗时。
    
    Args:
        tracer (Tracer): Jaeger等追踪器实例，用于追踪函数调用过程中的事件。
        func (Callable): 要执行的函数。
        *args: 可变位置参数，传递给func的参数。
        **kwargs: 可变关键字参数，传递给func的参数。
    
    Returns:
        Any: 函数func的返回值。
    
    """
    with tracer.start_as_current_span("Assistant-stream_run_with_handler", context=None) as span:
        parent_context = trace.set_span_in_context(span)
        span.set_attribute("openinference.span.kind",'Agent')
        start_time = time.time()
        result=func(*args, **kwargs)
        _input(args = args, kwargs = kwargs, span=span)
        if result:
            if hasattr(result, '_event_handler') and result._event_handler:
                event_handler = result._event_handler
                if hasattr(event_handler, '_iterator') and event_handler._iterator:
                    generator = event_handler._iterator
                    event_handler._iterator = _assistant_stream_run_with_handler_output(generator = generator, tracer = tracer, parent_context=parent_context)
            
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = span)
        return result

def _components_run_trace_with_opentelemetry(tracer, func, *args, **kwargs):
    """
    使用opentelemetry追踪组件运行过程
    
    Args:
        tracer (opentelemetry.trace.Tracer): OpenTelemetry追踪器对象
        func (callable): 需要追踪的函数
        *args: 任意数量的位置参数，用于调用func
        **kwargs: 任意数量的关键字参数，用于调用func
    
    Returns:
        Any: func函数的返回值
    
    """
    with tracer.start_as_current_span(_tool_name(args=args)) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'tool')
        _input(args = args, kwargs = kwargs, span=new_span)
        _components_run_output(output=result, span = new_span)
        return result

def _components_run_trace_with_sentry(func, *args, **kwargs):
    """
    使用 Sentry SDK 进行跟踪的函数装饰器。
    
    Args:
        func: 被装饰的函数对象。
        *args: 被装饰函数的参数，可变长度。
        **kwargs: 被装饰函数的命名参数，可变长度。
    
    Returns:
        函数 func 的执行结果。
    
    """
    try:
        import sentry_sdk
    except:
        raise ImportError("sentry-sdk is not installed.")
    
    with sentry_sdk.start_span(op=_tool_name(args=args), description=_tool_name(args=args)) as new_span:
        new_span.set_data("Span-kind", "Components-RUN")
        result=func(*args, **kwargs)
        _input(args = args, kwargs = kwargs, span=new_span)
        return result

def _components_stream_run_trace_with_opentelemetry(tracer, func, *args, **kwargs):
    """
    使用OpenTelemetry跟踪器追踪组件流运行过程
    
    Args:
        tracer (opentelemetry.trace.Tracer): OpenTelemetry跟踪器实例
        func (callable): 组件流函数
        *args: 组件流函数所需位置参数
        **kwargs: 组件流函数所需关键字参数
    
    Returns:
        Generator: 组件流函数返回值的生成器
    
    """
    with tracer.start_as_current_span(_tool_name(args = args)) as span:
        start_time = time.time()
        span.set_attribute("openinference.span.kind",'tool')
        _input(args = args, kwargs = kwargs, span=span)
        run_list = [] 
        for item in func(*args, **kwargs):  
            with tracer.start_as_current_span('Component-Stream') as new_span:  
                new_span.set_attribute("openinference.span.kind",'tool')
                if isinstance(item, ComponentOutput):
                    new_span.set_attribute("output.value", "{}".format(item.model_dump_json(indent=4)))
                else:
                    new_span.set_attribute("output.value", "{}".format(json.dumps(item, ensure_ascii=False)))
                    if isinstance(item, dict):
                        run_list.append(item.get('text', None))
                    else:
                        run_list.append(str(item))
                yield item
        end_time = time.time()  
        _time(start_time = start_time,end_time = end_time,span = span)
        if run_list:
            result_str = ''.join(str(res) for res in run_list)
            span.set_attribute("output.value",result_str)
        else:
            span.set_attribute("output.value","流式运行结束")

def _components_stream_run_trace_with_sentry(func, *args, **kwargs):
     """
     通过sentry追踪函数运行时的信息。
     
     Args:
         func (callable): 要执行的函数。
         *args: 可变位置参数，传入func的参数。
         **kwargs: 可变关键字参数，传入func的参数。
     
     Returns:
         Generator: 返回一个生成器，每次迭代返回func的一个返回值。
     
     """
     try:
         import sentry_sdk
     except:
         raise ImportError("sentry-sdk is not installed.")
     with sentry_sdk.start_span(op=_tool_name(args=args), description=_tool_name(args=args)) as span:
        span.set_data("Span-kind", "Components-Tool-Eval")
        _input(args = args, kwargs = kwargs, span=span)
        run_list = []
        for item in func(*args, **kwargs):  
            with sentry_sdk.start_span(op=_tool_name(args=args), description=_tool_name(args=args)) as new_span:  
                new_span.set_data("Span-kind",'tool')
                if isinstance(item, ComponentOutput):
                    new_span.set_data("output.value", "{}".format(item.model_dump_json(indent=4)))
                else:
                    new_span.set_data("output-value", "{}".format(json.dumps(item, ensure_ascii=False)))
                    if isinstance(item, dict):
                        text = item.get('text', None)
                        run_list.append(text)
                    else:
                        run_list.append(str(item))
                yield item
        if run_list: 
            result_str = ''.join(str(res) for res in run_list)
            span.set_data("output-value",result_str)
        else:
            span.set_data("output-value","流式运行结束")
                

def _list_trace(tracer, func, *args, **kwargs):
    """
    使用给定的tracer对函数func进行追踪，并记录相关信息到span中。
    
    Args:
        tracer (OpenTelemetryTracer): 用于追踪的tracer对象。
        func (Callable[..., Any]): 需要被追踪的函数。
        *args: 传递给func的位置参数。
        **kwargs: 传递给func的关键字参数。
    
    Returns:
        Any: 调用func的返回结果。
    
    """
    with tracer.start_as_current_span(_tool_name(args = args)) as new_span:      
        result=func(*args, **kwargs)
        new_span.set_attribute("openinference.span.kind",'tool')
        new_span.set_attribute("input.value",_tool_name(args = args))
        new_span.set_attribute("output.value",str(result))
    return result