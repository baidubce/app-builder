# AppBuilder SDK Components组件开发规范

组件（Component），是AppBuilder生态的重要组成部分，体现在Agent的能力边界，组件实现的规范性，稳定性，与用户最终的使用感受息息相关，下面详细介绍开发者需要关注的部分

## 开发示例

```python
class Component:
    """Component基类, 其它实现的Component子类需要继承该基类，并至少实现run方法、tool_eval方法，填写mainfest."""

    # 1、开发者必须填写的成员，mainfest，是对组件tool_eval方法的函数描述，包含了组件功能、函数入参等
    manifests = []
    
    # 2、开发这必须重载的成员函数，组件的__call__方法，与tool_eval方法，最终的底层实现都依赖于该函数
    def run(self, *inputs, **kwargs):
        Defines the computation performed at every call.
        Should be overridden by all subclasses.

        Parameters:
            *inputs(tuple): unpacked tuple arguments
            **kwargs(dict): unpacked dict arguments
        """
        raise NotImplementedError
        
    # 3、开发者必须重载的成员函数，Agent的FunctionCall调用的即是组件的tool_eval方法
    def tool_eval(self, **kwargs):
        if len(self.manifests) > 0:
            raise NotImplementedError
```

## 功能及详细要求

| 序号 | 功能点                                       | 详细要求                                                        |
| ---- | -------------------------------------------- | --------------------------------------------------------------- |
|1|成员 mainfest|要求必填，格式:  list[dict]，dict字段为
| |               |* "name"：str，要求不重复
| |               |* "description"：str，对于组件tool_eval函数功能的描述
| |               |* "parameters"：json_schema，对于tool_eval函数入参的描述，json_schema格式要求见https://json-schema.org/understanding-json-schema
| ---- | -------------------------------------------- | --------------------------------------------------------------- |
|2|run方法|要求必须实现，入参及出参要求为
| |               |* 入参为（*args，**kwargs），要求必须包含 
| |               |* * message：object Message，run所需内容包含在message.content中
| |               |* * stream：bool，支持流式返回
| |               |* 出参要求
| |               |* * 方法返回为 object Message
| |               |* * 若stream=True，则流式内容stream_events，用户需通过迭代器遍历message.content获取
| |               |* "name"：str，要求不重复
| ---- | -------------------------------------------- | --------------------------------------------------------------- |
|2|tool_eval方法|要求必须实现，入参及出参要求为
| |               |* 入参
| |               |* * 首先需要与mainfest中的json_schema匹配
| |               |* * 入参要求必须包含streaming参数，控制组件的流式/非流式返回
| |               |* 出参要求
| |               |* * 要求出参必须为str 类型，目的是配合Agent做FunctionCall，同时与Langchain的tool规范兼容
| |               |* * 需额外说明的是，部分组件需要返回 visible_scope字段，方便下游判断该组件结果为中间结果，还是用户最终可见结果