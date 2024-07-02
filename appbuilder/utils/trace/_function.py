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

def _time(start_time,end_time,span):
    span.set_attribute('time.cost-time',str(end_time-start_time)+'s')


def _build_curl_from_post(url, headers, json_body, timeout) -> str:
        """
        Generate cURL command from post request parameters.
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

    curl=_build_curl_from_post(
        url=args[-1], 
        headers=kwargs['headers'], 
        json_body=kwargs.get('json',None), 
        timeout=kwargs.get('timeout',None), 
        )
    span.set_attribute("input.value","{}".format(curl))


def _client_input(args,kwargs,span):
    input_dict={}
    type_name = (bool,str,bytes,int,float,list,dict)
    sig = inspect.signature(args[0])
    params = sig.parameters
    try:
        if args:
            for idx, value in enumerate(list(args)):
                if isinstance(value, type_name):
                    input_dict[list(params)[idx-1]] = str(value)
        if kwargs:
            for key, value in dict(kwargs).items():
                if isinstance(value, type_name):
                    input_dict[key] = str(value)

        span.set_attribute("input.value",json.dumps(input_dict, ensure_ascii=False))
    except Exception as e:
        print(e)


def _client_run_trace_output(output,span,tracer):
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
                result += message.answer
                
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
    for item in run_list:
        yield item

def _client_tool_trace_output_deep_iterate(output,span):
    input_dict={}
    type_name = (bool,str,bytes,int,float,list,dict)
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


def _client_tool_trace_output(output, span):
    if inspect.isclass(output):
        output_dict = output.__dict__
        _client_tool_trace_output_deep_iterate(output=output_dict,span=span)
    else:
        _client_tool_trace_output_deep_iterate(output=output,span=span)


def _tool_name(args):

    class_name = args[0].__qualname__.split('.')[0]
    function_name = args[0].__name__
    if class_name == function_name:
        return "{}".format(function_name) 
    else:
        return "{}-{}".format(class_name,function_name)
    

def _post_trace(tracer, func, *args, **kwargs):
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
    with tracer.start_as_current_span('AppBuilderClient-RUN') as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'Agent')
        _client_input(args = args, kwargs = kwargs, span=new_span)
        generator_list = _client_run_trace_output(output=result,span = new_span,tracer=tracer)
        
    
    if generator_list:
        result.content = _return_generator(generator_list)
        return result
    else:
        return result

def _client_tool_trace(tracer, func, *args, **kwargs):
    with tracer.start_as_current_span(_tool_name(args=args)) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'tool')
        _client_tool_trace_output(output=result, span = new_span)
    return result
        