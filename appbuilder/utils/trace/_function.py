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
import time
import json
import inspect
from typing import Generator
from pydantic import BaseModel
from appbuilder import Message

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
            span.set_attribute("input.value",json.dumps(input_dict, ensure_ascii=False))
    except Exception as e:
        print(e)


def _client_run_trace_output(output,span,tracer):
    """
    根据给定的输出、span和tracer，记录并处理客户端的trace输出信息。
    
    Args:
        output (Any): 客户端的输出信息，可能是一个生成器或AppBuilderClientAnswer对象。
        span (Span): Jaeger的Span对象，用于记录trace信息。
        tracer (Tracer): Jaeger的Tracer对象，用于创建新的Span。
    
    Returns:
        list: 如果output是生成器类型，则返回生成器中的消息列表；否则返回空列表。
    
    """
    if output:
        run_list = []
        generator_list = []
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        if output.mtype == 'generator':
            result = ''
            new_span = tracer.start_span('Client-Stream')
            for message in output.content:
                new_span.set_attribute("openinference.span.kind",'agent')
                generator_list.append(message)

                context_message_str=""
                has_reference = False
                if hasattr(message, 'events') and message.events and hasattr(message.events[0], 'detail') and message.events[0].detail:
                    context_message_list = message.events[0].detail.get('references',None)
                if context_message_list:
                    for context_message in context_message_list:
                        for context_message_key,context_message_value in context_message.items():
                            context_message_str += '{}: {}\n'.format(context_message_key, context_message_value)
                            has_reference = True
                        context_message_str +='\n'
                if has_reference:
                    new_span.set_attribute("input.value", 'Context(上下文) For RAG:\n{}'.format(context_message_str))
                try:
                    new_span.set_attribute("output.value", "{}".format(message.model_dump_json(indent=4)))
                except Exception as e:
                    print(e)
                result += str(message.answer)
                
                if hasattr(message, 'events') and message.events and hasattr(message.events[0], 'event_type') and hasattr(message.events[0], 'status'):
                    run_list.append('{}[status:{}]'.format(message.events[0].event_type,message.events[0].status))
                
                if hasattr(message, 'events') and message.events and hasattr(message.events[0], 'usage') and message.events[0].usage and hasattr(message.events[0].usage, 'prompt_tokens'):   
                    prompt_tokens = message.events[0].usage.prompt_tokens
                    completion_tokens = message.events[0].usage.completion_tokens
                    total_tokens = message.events[0].usage.total_tokens
                
                new_span.end()
                new_span = tracer.start_span('Client-Stream')
            
            new_span.set_attribute("output.value",'流式输出结束:\n输出结果为:{}'.format(result))
            new_span.set_attribute("openinference.span.kind",'agent')
            new_span.end()

            span.set_attribute("output.value",result)
        elif output.mtype == 'AppBuilderClientAnswer':
            span.set_attribute("output.value",output.content.answer)
            events = output.content.events
            for event in events:
                run_list.append('{}[status:{}]'.format(event.event_type,event.status))
                if hasattr(event, 'usage') and event.usage and hasattr(event.usage, 'prompt_tokens'):
                    prompt_tokens += event.usage.prompt_tokens
                    completion_tokens += event.usage.completion_tokens
                    total_tokens += event.usage.total_tokens

        if total_tokens:
            span.set_attribute("llm.token_count.prompt",prompt_tokens)
            span.set_attribute("llm.token_count.completion", completion_tokens)
            span.set_attribute("llm.token_count.total", total_tokens)
        span.set_attribute("Agent-Running-Process",'==>'.join(run_list))

    return generator_list

def _return_generator(run_list) -> Generator:
    """
    返回一个生成器，逐个生成并返回run_list中的元素。
    
    Args:
        run_list (list): 包含要生成的元素的列表。
    
    Returns:
        Generator: 返回一个生成器，用于逐个生成并返回run_list中的元素。
    
    """
    for item in run_list:
        yield item

def _client_tool_trace_output_deep_iterate(output,span):
    """
    对客户端工具的输出进行深度迭代，并设置OpenTelemetry的span属性。
    
    Args:
        output (Union[dict, bool, str, bytes, int, float, list]): 客户端工具的输出结果，可以是字典、布尔值、字符串、字节串、整数、浮点数或列表。
        span (Span): OpenTelemetry的span对象，用于设置span属性。
    
    Returns:
        None: 此函数不返回任何值，但会设置span的"output.value"属性。
    
    Raises:
        无特定异常，但会捕获并打印所有在函数执行过程中发生的异常。
    
    """
    input_dict={}
    type_name = (bool,str,bytes,int,float,list)
    try:    
        if isinstance(output, dict):
            for key, value in dict(output).items():
                if isinstance(value, type_name):
                    input_dict[key] = str(value)
            span.set_attribute("output.value",json.dumps(input_dict, ensure_ascii=False))
        else:
            if isinstance(output, type_name):
                span.set_attribute("output.value",str(output))
    except Exception as e:
        print(e)


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
            new_span = tracer.start_span('Client-Stream')
        for item in run_list:
            result += str(item) 
        new_span.set_attribute("output.value",'流式输出结束\n输出结果为:{}'.format(result))
        new_span.set_attribute("openinference.span.kind",'agent')
        new_span.end()
        span.set_attribute("output.value",result)
    return generator_list

def _assistant_stream_run_with_handler_output(output,span,tracer):
    """
    处理带有事件处理器的输出流，并生成相关的span和输出列表。
    
    Args:
        output (Any): 事件处理器的输出对象，包含_event_handler属性。
        span (Span): 追踪的span对象。
        tracer (Tracer): 追踪器对象。
    
    Returns:
        None: 该函数没有返回值，但会修改传入的output对象的_event_handler._iterator属性。
    
    """
    result = ''
    output_list = []
    generator_list = []
    if output:
        new_span = tracer.start_span('Assistant-Stream_run_with_handler')
        if hasattr(output, '_event_handler') and output._event_handler:
            event_handler = output._event_handler
            if hasattr(event_handler, '_iterator') and event_handler._iterator:
                for message in event_handler._iterator:
                    generator_list.append(message)
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
                new_span.set_attribute("output.value",'流式运行结束')
                new_span.set_attribute("openinference.span.kind",'agent')   
                new_span.end()
                for item in output_list:
                    result += str(item)
                span.set_attribute("output.value", result)
                output._event_handler._iterator = _return_generator(generator_list)

    return output

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

def _components_stream_output(output, span, tracer):
    """
    将组件的输出流转换为字符串并返回生成器列表。
    
    Args:
        output (Iterable[Any]): 组件的输出流，可以是任何可迭代对象。
        span (opentelemetry.trace.Span): 当前追踪的span对象。
        tracer (opentelemetry.trace.Tracer): 追踪器对象，用于创建span。
    
    Returns:
        List[Any]: 组件输出流的生成器列表。
    
    """
    result = ''
    run_list = []
    generator_list = []
    if output:
        for message in output:
            with tracer.start_as_current_span('Component-Stream') as new_span:
                new_span.set_attribute("openinference.span.kind",'agent')
                generator_list.append(message)
                new_span.set_attribute("openinference.span.kind",'tool')
                new_span.set_attribute("output.value", "{}".format(json.dumps(message, ensure_ascii=False)))
                if isinstance(message, dict):
                    run_list.append(message.get('text', None))
                else:
                    try:
                        run_list.append(str(message))
                    except:
                        print("message can't to be str")
        for item in run_list:
            result += str(item) 
        span.set_attribute("output.value",result)
    return generator_list     

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
    跟踪客户端运行函数，并添加跟踪信息。
    
    Args:
        tracer (Any): 跟踪器对象，用于生成和追踪span。
        func (Callable[..., Any]): 需要跟踪的函数。
        *args: 可变位置参数，func函数的输入参数。
        **kwargs: 可变关键字参数，func函数的输入参数。
    
    Returns:
        Any: func函数的返回结果，若函数返回结果是generator类型，则将其转换为列表后返回。
    
    """
    with tracer.start_as_current_span('AppBuilderClient-RUN') as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'Agent')
        _input(args = args, kwargs = kwargs, span=new_span)
        generator_list = _client_run_trace_output(output=result,span = new_span,tracer=tracer)
        
    if generator_list:
        result.content = _return_generator(generator_list)
        return result
    else:
        return result

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
    为给定函数func添加分布式追踪功能，记录函数执行时间、参数、返回值等信息，并生成对应的追踪span。
    
    Args:
        tracer (Tracer): 分布式追踪器对象，用于生成span。
        func (Callable[..., Any]): 要被追踪的函数。
        *args: 函数func的位置参数。
        **kwargs: 函数func的关键字参数。
    
    Returns:
        Any: 函数func的返回值，如果func返回的是生成器类型，则返回一个封装了生成器的对象。
    
    """
    with tracer.start_as_current_span("Assistant-stream_run") as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'Agent')
        _input(args = args, kwargs = kwargs, span=new_span)
        generator_list = _assistant_stream_output(output=result, span = new_span, tracer=tracer)
        if generator_list:
            result = _return_generator(generator_list)
    return result

def _assistant_stream_run_with_handler_trace(tracer, func, *args, **kwargs):
    """
    为给定函数func添加分布式追踪功能，记录函数执行时间、参数、返回值等信息，并生成对应的追踪span。
    
    Args:
        tracer (Tracer): 分布式追踪器对象，用于生成span。
        func (Callable[..., Any]): 要被追踪的函数。
        *args: 函数func的位置参数。
        **kwargs: 函数func的关键字参数。
    
    Returns:
        Any: 函数func的返回值，如果func返回的是生成器类型，则返回一个封装了生成器的对象。
    
    """
    with tracer.start_as_current_span("Assistant-stream_run_with_handler") as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'Agent')
        _input(args = args, kwargs = kwargs, span=new_span)
        result = _assistant_stream_run_with_handler_output(output=result, span = new_span, tracer=tracer)
    return result

def _components_run_trace(tracer, func, *args, **kwargs):
    """
    追踪组件执行的函数装饰器。
    
    Args:
        tracer (Tracer): 追踪器对象，用于创建和管理跟踪的span。
        func (Callable[..., Any]): 要追踪的函数。
        *args: 可变数量的位置参数，传递给func。
        **kwargs: 可变数量的关键字参数，传递给func。
    
    Returns:
        Any: func函数执行后的结果。
    
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

def _components_stream_run_trace(tracer, func, *args, **kwargs):
    """
    跟踪组件流执行过程的装饰器函数。
    
    Args:
        tracer (Tracer): 追踪器对象，用于创建和操作追踪的span。
        func (Callable): 需要被追踪的函数。
        *args: 可变参数列表，传入func的参数。
        **kwargs: 关键字参数列表，传入func的参数。
    
    Returns:
        Any: func函数执行后的返回值，如果返回值是生成器类型，则会被转换成迭代器类型。
    
    """
    with tracer.start_as_current_span(_tool_name(args=args)) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'tool')
        _input(args = args, kwargs = kwargs, span=new_span)
        generator_list = _components_stream_output(output=result, span = new_span, tracer=tracer)
        if generator_list:
            result = _return_generator(generator_list)
    return result

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
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        new_span.set_attribute("openinference.span.kind",'tool')
        new_span.set_attribute("input.value",_tool_name(args = args))
        new_span.set_attribute("output.value",str(result))
    return result

    
        