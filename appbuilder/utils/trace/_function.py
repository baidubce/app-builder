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
import appbuilder

appbuilder.logger

def _time(start_time,end_time,span):
    span.set_attribute('time.cost-time',str(end_time-start_time)+'s')


def _post_input(args,kwargs,span):
    type_name = (bool,str,bytes,int,float)
    if kwargs:
        for key,value in kwargs.items():
                if key == 'json':
                    for json_key,json_value in value.items():
                        if isinstance(json_value,type_name):
                            span.set_attribute("input.value.json."+json_key,str(json_value))
                        else:
                            try:
                                span.set_attribute("input.value.json."+json_key,str(json_value))
                            except:
                                pass

                elif key == 'headers':
                    for header_key,header_value in value.items():
                        if header_key in ('Content-Type','Authorization'):
                            continue
                        if isinstance(header_value,type_name):
                            span.set_attribute("input.value.headers."+header_key,str(header_value))
                        else:
                            try:
                                span.set_attribute("input.value.headers."+header_key,str(header_value))
                            except:
                                pass


def _post_output(output,span):
    pass


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
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        if output.mtype == 'generator' :
            result = ''
            new_span = tracer.start_span('Client-Stream')
            for message in output.content:
                # print(message)
                new_span.set_attribute("openinference.span.kind",'agent')
                try:
                    new_span.set_attribute("output.value", '{}[status:{}]:{}'.format(message.events[0].event_type,message.events[0].status,message.answer))
                    new_span.set_attribute("LLM-RUN-Information."+'prompt-tokens', message.events[0].usage.prompt_tokens)
                    new_span.set_attribute("LLM-RUN-Information."+'completion-tokens', message.events[0].usage.completion_tokens)
                    new_span.set_attribute("LLM-RUN-Information."+'total-tokens', message.events[0].usage.total_tokens)
                    new_span.set_attribute("LLM-RUN-Information."+'LLM-Name', message.events[0].usage.name)
                    new_span.set_attribute("input.value", '此阶段调用模型(LLM):{}'.format(message.events[0].usage.name))
                except:pass 
                result += message.answer
                try:
                    run_list.append('{}[status:{}]'.format(message.events[0].event_type,message.events[0].status))
                except:pass
                try:
                    prompt_tokens = message.events[0].usage.prompt_tokens
                    completion_tokens = message.events[0].usage.completion_tokens
                    total_tokens = message.events[0].usage.total_tokens
                except:pass
                
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
                try:
                    prompt_tokens += event.usage.prompt_tokens
                    completion_tokens += event.usage.completion_tokens
                    total_tokens += event.usage.total_tokens
                except:pass
        if total_tokens:
            span.set_attribute("llm.token_count.prompt",prompt_tokens)
            span.set_attribute("llm.token_count.completion", completion_tokens)
            span.set_attribute("llm.token_count.total", total_tokens)
        span.set_attribute("Agent-Running-Process",'==>'.join(run_list))


def _post_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    func = new_func 
    with tracer.start_as_current_span("HTTP-POST") as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        new_span.set_attribute("openinference.span.kind",'chain')
        _time(start_time = start_time,end_time = end_time,span = new_span)
        _post_input(args = args, kwargs = kwargs,span = new_span)
        _post_output(output = result,span = new_span)

    return result

def _client_run_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    func = new_func 
    with tracer.start_as_current_span('AppBuilderClient-RUN') as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _time(start_time = start_time,end_time = end_time,span = new_span)
        new_span.set_attribute("openinference.span.kind",'Agent')
        _client_run_trace_output(output=result,span = new_span,tracer=tracer)
        _client_input(args = args, kwargs = kwargs, span=new_span)
    return result


        