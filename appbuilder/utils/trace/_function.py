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

from appbuilder.core.message import Message


def _qualname(qualname):
    return "{}({})".format(qualname[-1],qualname[0])


def _time(start_time,end_time,span):
    span.set_attribute('time.cost-time',str(end_time-start_time)+'s')


def _span_kind(module_name,span):
    model_name = module_name.split('.')
    span.set_attribute('openinference.span.kind','tool')
    if 'console' in model_name:
        span.set_attribute('openinference.span.kind','agent')
        if 'dataset' in model_name:
            span.set_attribute('openinference.span.kind','tool')
    elif 'assistant' in model_name:
        span.set_attribute('openinference.span.kind','agent')
    elif 'embeddings' in model_name:
        span.set_attribute('openinference.span.kind','embedding')
    elif 'retriever' in model_name:
        span.set_attribute('openinference.span.kind','retriever')
    elif 'llms' in model_name:
        span.set_attribute('openinference.span.kind','chain')


def _deep_retrieve(name, value, span):
    """
    递归地将复杂数据类型(list, dict)转换为字符串。
    处理 bool, str, bytes, int, float 形式的基本类型。
    """
    print("value: {}".format(value))
    if isinstance(value, (bool, bytes, int, float)):
        span.set_attribute(name, value)
    elif isinstance(value, str):
        # 转为utf-8 编码的字符串
        span.set_attribute(name, value.encode("utf-8").decode())
    elif isinstance(value, Message):
        span.set_attribute(f"{name}.id", value.id if value.id else 'None')
        span.set_attribute(f"{name}.Message-name", value.name if value.name else 'None')
        span.set_attribute(f"{name}.Message-type", value.mtype if value.mtype else 'None')
        if value.content:
            _deep_retrieve(name=f"{name}.value", value = value.content, span = span)    
    elif isinstance(value, dict):
        try:
            # 将字典转换为 JSON 字符串
            for key, val in value.items():
                _deep_retrieve(name=f"{name}.{key}", value = val, span = span)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Unable to serialize dict: {e}")
    elif isinstance(value, list):
        try:
            # 将列表转换为 JSON 字符串
            for index, item in enumerate(value):
                _deep_retrieve(name=f"{name}[{index}]", value = item, span = span)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Unable to serialize list: {e}")
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")



def _input(args,kwargs,span):
    if kwargs:
        for key,value in kwargs.items():
            if isinstance(value,Message):
                span.set_attribute('input.id',value.id if value.id else 'None') 
                span.set_attribute('input.Message-name',value.name if value.name else 'None')
                span.set_attribute('input.Message-type',value.mtype if value.mtype else 'None')
                if not value.content :
                    continue
                _deep_retrieve(name='input.value', value=value, span = span)
                

    if args:
        for value in args:
            if isinstance(value,Message):
                span.set_attribute('input.id',value.id if value.id else 'None') 
                span.set_attribute('input.Message-name',value.name if value.name else 'None')
                span.set_attribute('input.Message-type',value.mtype if value.mtype else 'None')
                if not value.content :
                    continue
                _deep_retrieve(name='input.value', value=value, span = span)


def _output(output,span):

    if isinstance(output,Message):
        span.set_attribute('output.id',output.id if output.id else 'None')
        span.set_attribute('output.Message-name',output.name if output.name else 'None')
        span.set_attribute('output.Message-type',output.mtype if output.mtype else 'None')
        if output.content:
            span.set_attribute('output.value',str(output.content))
        else:
            span.set_attribute('output.value','None')
        try:
            if output.token_usage:
                token_usage = output.token_usage
                span.set_attribute("llm.token_count.prompt",token_usage.get('prompt_tokens',0))
                span.set_attribute("llm.token_count.completion", token_usage.get('completion_tokens',0))
                span.set_attribute("llm.token_count.total", token_usage.get('total_tokens',0))
        except:
            span.set_attribute("llm.token_count.prompt",0)
            span.set_attribute("llm.token_count.completion", 0)
            span.set_attribute("llm.token_count.total", 0)


def _tool_eval_input(args,kwargs,span):
    args_type_name = (bool,str,bytes,int,float,list,dict)
    if args:
        input_list=[]
        for value in args:
            if isinstance(value,args_type_name):
                input_list.append(str(value))
        if input_list:
            span.set_attribute("input.value",json.dumps(input_list))

    default_key=('name','streaming')
    type_name = (bool,str,bytes,int,float)
    if kwargs:
        for key,value in kwargs.items():
            if key not in default_key :
                if isinstance(value,type_name):
                    span.set_attribute("input.value."+key,value)
                else:
                    try:
                        span.set_attribute("input.value."+key,json.dumps(value))
                    except:
                        span.set_attribute("input.value."+key,str(value))
            else:
                span.set_attribute('input.'+key, value)
    

def _tool_eval_output(output,span):
    if isinstance(output,dict):
        for key,value in output.items():
            if key == 'text':
                span.set_attribute('output.text',str(value))
            else:
                span.set_attribute('output.'+key, value)


def _assistant_input(args,kwargs,span):
    type_name = (bool,str,bytes,int,float,list,dict)
    if args:
        input_list=[]
        for value in args:
            if isinstance(value,type_name):
                input_list.append(str(value))
        if input_list:
            span.set_attribute("input.value",json.dumps(input_list))
            
    if kwargs:   
        for key,value in kwargs.items():
            type_name = (bool,str,bytes,int,float)
            if isinstance(value,type_name):
                span.set_attribute("input.value."+key,value)
            elif isinstance(value,(dict,list)):
                span.set_attribute("input.value."+key,str(value))
            


def _assistant_output(output,span):
    output_dict = output.__dict__
    op_dict={}
    type_name = (bool,str,bytes,int,float,dict,list)
    for key,value in output_dict.items(): 
        if isinstance(value,type_name):
            op_dict[key]=str(value)
    span.set_attribute("output.value",json.dumps(op_dict))
            


def _client_input(args,kwargs,span):
    input_dict={}
    type_name = (bool,str,bytes,int,float,list,dict)
    sig = inspect.signature(args[0])
    params = sig.parameters
    print("!!!params ", params)
    print("!!!value: ", json.dumps(input_dict, ensure_ascii=False))
    print(args)
    if args:
        for idx, value in enumerate(args):
            print(idx, value)
            if isinstance(value, type_name):
                print(params[idx], value)
                input_dict[params[idx]] = str(value).encode("utf-8").decode()
                print("input_dict: ", input_dict)
    print("!!!value: ", json.dumps(input_dict, ensure_ascii=False))
    print(kwargs)
    if kwargs:
        for key, value in kwargs:
            if isinstance(value, type_name):
                input_dict[key] = str(value).encode("utf-8").decode()
                print("input_dict: ", input_dict)
        # span.set_attribute("input.value",json.dumps(input_dict, ensure_ascii=False))
    
    print("!!!value: ", json.dumps(input_dict, ensure_ascii=False))
    span.set_attribute("input.value",json.dumps(input_dict, ensure_ascii=False))

def _tip(span):
    span.set_attribute('tips','注意:若输入为默认值，则不记录')


def _run_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    module_name = args[1].__module__
    qualname = func.__qualname__.split('.') 
    func = new_func           
    # trace for run
    with tracer.start_as_current_span(_qualname(qualname=qualname)) as new_span:
        start_time = time.time()
        result = func(*args,**kwargs) 
        end_time = time.time()
        _time(start_time=start_time,end_time=end_time,span=new_span)
        _span_kind(module_name=module_name,span=new_span)
        _input(args=args,kwargs=kwargs,span=new_span)
        _tip(span=new_span)
        _output(output=result,span=new_span)
        if 'CompletionBaseComponent' in qualname:
            new_span.set_attribute('openinference.span.kind','llm')
        else: 
            if 'llms' in module_name:
                new_span.set_attribute("llm.token_count.prompt",0)
                new_span.set_attribute("llm.token_count.completion", 0)
                new_span.set_attribute("llm.token_count.total", 0)
        if 'appbuilder_client' in module_name:
            try:
                _client_input(args=args, kwargs = kwargs,span=new_span)
            except:
                pass
    return result 


def _tool_eval_streaming_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    module_name = args[1].__module__
    qualname = func.__qualname__.split('.') 
    func = new_func  
    # trace for tool_eval
    with tracer.start_as_current_span(qualname[0]) as new_span:
        start_time = time.time()
        gen=func(*args, **kwargs)
        end_time = time.time()
        new_span.set_attribute("openinference.span.kind",'chain')
        _time(start_time=start_time,end_time=end_time,span=new_span)
        new_span.set_attribute("streaming", 'True')
        _tool_eval_input(args=args,kwargs=kwargs,span=new_span)
        _tip(span=new_span)

        for value in gen:
            with tracer.start_as_current_span(qualname[-1]) as new_span_tool_eval:
                if 'llms' in module_name:
                    new_span_tool_eval.set_attribute("openinference.span.kind",'chain')
                else:    
                    _span_kind(module_name=module_name,span=new_span_tool_eval)
                _tip(span=new_span_tool_eval)
                _tool_eval_output(output=value,span=new_span_tool_eval)
                _tool_eval_output(output=value,span=new_span)
                yield value


def _assistant_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    module_name = args[1].__module__
    qualname = func.__qualname__.split('.') 
    func = new_func 
    # trace for assistant
    with tracer.start_as_current_span(_qualname(qualname=qualname)) as new_span:
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        _span_kind(module_name=module_name,span=new_span)
        _time(start_time = start_time,end_time = end_time,span = new_span)
        _assistant_input(args = args, kwargs = kwargs,span = new_span)
        if result:
            _assistant_output(output = result,span = new_span)
        _tip(span=new_span)

    return result
