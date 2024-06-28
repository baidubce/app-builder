# Appbuilder-SDK Trace模块开发人员要求

## components组件部分

### run函数

- run函数的传入传出参数需要严格按照Appbuilder-SDK的run函数参数要求
- 在run函数开发完成后需要使用run_trace装饰器进行装饰

```python
from appbuilder.utils.trace.tracer_wrapper import run_trace

@run_trace
def run():
    pass
```

### tool_eval函数

- tool_eval函数的传入传出参数需要严格按照Appbuilder-SDK的tool_eval函数参数要求
- 在tool_eval函数开发完成后需要使用装饰器进行装饰

```python
from appbuilder import tool_eval_streaming_trace

@tool_eval_streaming_trace
def tool_eval():
    pass
```

## assistant api组件部分

- assistant api组件函数的开发需要使用装饰器进行装饰

```python
from appbuilder.utils.trace.tracer_wrapper import assistant_trace

@assistant_trace
class Assistant():
    def create():
        pass
```

## console组件部分

### run函数

- run函数的传入传出参数需要严格按照Appbuilder-SDK的run函数参数要求
- 在run函数开发完成后需要使用run_trace装饰器进行装饰

```python
from appbuilder.utils.trace.tracer_wrapper import run_trace

@run_trace
def run():
    pass
```

### dataset函数

- dataset文件内函数的结构特殊性，因此使用assistant_trace装饰器实现装饰

```python
from appbuilder.utils.trace.tracer_wrapper import assistant_trace

@assistant_trace
def create_dataset():
    pass
```

## 总结

- 以Message为载体进行数据传输，依据信息传输方式，使用run_trace和tool_eval_streaming_trace装饰器
- 其他的函数使用assistant_trace装饰器进行装饰
- 开发新模块需要查看trace模块_function.py文件的_span_kind函数，确认新加模块的种类是否符合预期