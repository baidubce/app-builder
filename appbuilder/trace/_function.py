import time
import json

from appbuilder.core.message import Message


def _qualname(qualname):
    return "{}({})".format(qualname[-1],qualname[0])


def _time(start_time,end_time,span):
    span.set_attribute('time.cost-time',str(end_time-start_time)+'s')


def _span_kind(module_name,span):
    module_name = module_name.split('.')
    if 'components' in module_name:
        span_kind = 'tool'
        if 'embeddings' in module_name:
            span_kind = 'Embedding'
        elif 'retriever' in module_name:
            span_kind = 'Retriever'
        elif 'llms' in module_name:
            span_kind = 'LLM'
    elif 'rag' in module_name:
        span_kind = 'Retriever'
    elif 'appbuilder_client' in module_name:
        span_kind = 'agent'
    elif 'assistant' in module_name:
        span_kind = 'chain'
    span.set_attribute('openinference.span.kind',span_kind)
    

def _deep_dist(name,message_dict,span):
    type_name = (bool,str,bytes,int,float)
    for key, value in message_dict.items():
        if isinstance(value, dict):
            name = name+'.'+key
            _deep_dist(name=name, message_dict=value, span=span)
        else:
            _name = name+'.'+key
            if isinstance(value,type_name):
                span.set_attribute(_name,value)
            else:
                try:
                    span.set_attribute(_name,json.dumps(value))
                except:
                    span.set_attribute(_name,value)

def _input(args,kwargs,span):
    type_name = (bool,str,bytes,int,float)
    if kwargs:
        for key,value in kwargs.items():
            if isinstance(value,Message):
                span.set_attribute('input.id',value.id if value.id else 'None') 
                span.set_attribute('input.Message-name',value.name if value.name else 'None')
                span.set_attribute('input.Message-type',value.mtype if value.mtype else 'None')
                if not value.content :
                    continue
                if isinstance(value.content,dict):
                    _deep_dist(name='input.value',message_dict=value.content,span=span)
                else :
                    if isinstance(value,type_name):
                        span.set_attribute("input.value."+key,value)
                    else:
                        try:
                            span.set_attribute("input.value."+key,json.dumps(value))
                        except:
                            span.set_attribute("input.value."+key,str(value))
                

    if args:
        for value in args:
            if isinstance(value,Message):
                span.set_attribute('intput.id',value.id if value.id else 'None') 
                span.set_attribute('input.Message-name',value.name if value.name else 'None')
                span.set_attribute('input.Message-type',value.mtype if value.mtype else 'None')
                if not value.content :
                    continue
                if isinstance(value.content,dict):
                    _deep_dist(name='input.value',message_dict=value.content,span=span)
                else :
                    if isinstance(value,type_name):
                        span.set_attribute("input.value",value)
                    else:
                        try:
                            span.set_attribute("input.value",json.dumps(value))
                        except:
                            span.set_attribute("input.value",str(value))


def _output(output,span):

    if isinstance(output,Message):
        span.set_attribute('output.id',output.id if output.id else 'None')
        span.set_attribute('output.Message-name',output.name if output.name else 'None')
        span.set_attribute('output.Message-type',output.mtype if output.mtype else 'None')
        if output.content:
            if isinstance(output.content,dict):
                _deep_dist(name='output.value',message_dict=output.content,span=span)
            else :
                span.set_attribute('output.value',output.content if output.content or output.content == 0 or output.content ==0.0 or output.content == False else 'None')
        else:
            span.set_attribute('output.value','Null')
        try:
            if output.extra:
                _deep_dist(name='output.extra',message_dict=output.extra,span=span)
            else:
                span.set_attribute('output.extra','{}')
        except:
            span.set_attribute('output.extra','Null')
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


def _tool_eval_input(arg,kwary,span):
    default_key=('name','streaming')
    type_name = (bool,str,bytes,int,float)
    for key,value in kwary.items():
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
                type_name = (bool,str,bytes,int,float)
                if isinstance(value,type_name):
                    span.set_attribute("output."+key,value)
                elif isinstance(value,dict):
                    _deep_dist(name='output.'+key,message_dict=value,span=span)
                elif isinstance(value,list):
                    span.set_attribute("output."+key,json.dumps(value))
                else:
                    try:
                        span.set_attribute("output."+key,json.dumps(value.__dict__))
                    except:
                        pass
            else:
                span.set_attribute('output.'+key, value)
    if isinstance(output,str):
        span.set_attribute('output.value', output)


def _assistant_input(input,span):
    for key,value in input.items():
        type_name = (bool,str,bytes,int,float)
        if isinstance(value,type_name):
            span.set_attribute("input."+key,value)
        elif isinstance(value,dict):
            _deep_dist(name='input.'+key,message_dict=value,span=span)
        elif isinstance(value,list):
            span.set_attribute("input."+key,json.dumps(value))


def _assistant_output(output,span):
    output_dict = output.__dict__
    for key,value in output_dict.items():
        type_name = (bool,str,bytes,int,float)
        if isinstance(value,type_name):
            span.set_attribute("output."+key,value)
        elif isinstance(value,dict):
            _deep_dist(name='output.'+key,message_dict=value,span=span)
        elif isinstance(value,list):
            span.set_attribute("output."+key,json.dumps(value))
        else:
            try:
                span.set_attribute("output."+key,json.dumps(value.__dict__))
            except:
                pass

        
def _tip(span):
    span.set_attribute('tips','注意:若输入为默认值，则不记录')

def _run_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    module_name = args[-1].__module__
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
    return result 


def _tool_eval_streaming_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    module_name = args[-1].__module__
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
        _tool_eval_input(arg=args,kwary=kwargs,span=new_span)
        _tip(span=new_span)

        for value in gen:
            with tracer.start_as_current_span(qualname[-1]) as new_span_tool_eval:
                _span_kind(module_name=module_name,span=new_span_tool_eval)
                _tip(span=new_span_tool_eval)
                _tool_eval_output(output=value,span=new_span_tool_eval)
                _tool_eval_output(output=value,span=new_span)
                yield value



def _assistant_trace(tracer, func, *args, **kwargs):
    new_func = func
    func=args[0]
    module_name = args[-1].__module__
    qualname = func.__qualname__.split('.') 
    func = new_func 
    # trace for assistant
    with tracer.start_as_current_span(_qualname(qualname=qualname)) as new_span:
        start_time = time.time()
        if 'download' in qualname:
            func(*args, **kwargs)
        else:
            result=func(*args, **kwargs)
            _assistant_output(output=result,span=new_span)
        end_time = time.time()
        _span_kind(module_name=module_name,span=new_span)
        _time(start_time=start_time,end_time=end_time,span=new_span)
        _assistant_input(input = kwargs,span=new_span)
        _tip(span=new_span)

    return result
