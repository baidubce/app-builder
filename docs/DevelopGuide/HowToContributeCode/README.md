# SDK 贡献代码规范

## 组件开发规范

### 组件整体介绍

 在无特殊情况下，一个官方组件（class Component）的实现可以拆解为以下几个关键模块，分别是
* 1、def run：组件的run函数，规范体现在该函数的输入和输出
  * 输入规范
  * 输出规范
* 2、def tool_eval：组件功能的核心实现，规范体现在该函数的输入和输出
  * 输入规范
  * 输出规范
* 3、dict manifest：组件参与FunctionCall时，帮助大模型理解组件功能的说明，规范体现在manifest的内容和格式
  * manifest规范

### `run` 函数

#### 消息(Message)
- 构建大模型应用的统一数据结构，基于Pydantic构建，在不同的Component之间流动。Message基类的默认字段是content，类型是Any。
```python
from appbuilder import Message
input_dict = Message({"query": "红烧肉怎么做"})
input_list = Message(["text1", "text2", "text3"])
input_str = Message("红烧肉怎么做")
```

#### `run` 函数输入输出规范

- 所有能力单元的标准结构，以Message结构作为输入输出，内部执行逻辑可在本地执行或调用云端服务，以下是官方组件的实现示例。`run` 函数需要添加 `@components_run_trace` 装饰器，实现对组件的trace。

```python
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

class SimilarQuestionMeta(ComponentArguments):
    """ SimilarQuestionMeta
    """
    message: Message = Field(..., 
                             variable_name="query", 
                             description="输入消息，用于模型的输入，一般为问题。")


class SimilarQuestion(CompletionBaseComponent):
    """ 基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
    Examples:

        .. code-block:: python
            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = "..."

            qa_mining = appbuilder.SimilarQuestion(model="Qianfan-Agent-Speed-8k")

            msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
            msg = appbuilder.Message(msg)
            answer = qa_mining(msg)

            print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    def __init__(self, model=None):
        """初始化SimilarQuestionMeta任务。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
        
        Returns:
            None
        
        """
        super().__init__(SimilarQuestionMeta, model=model)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10):
        """
        给定输入（message）到模型运行，同时指定运行参数，并返回结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature)
```

### `tool_eval` 函数

#### `ComponentOutput` 类

```python
class ComponentOutput(BaseModel):
    role: str = Field(default="tool",
                      description="role是区分当前消息来源的重要字段，对于绝大多数组件而言，都是填写tool，标明role所在的消息来源为组件。部分思考及问答组件，role需要填写为assistant")
    content: list[Content] = Field(default=[],
                                         description="content是当前组件返回内容的主要payload，List[Content]，每个Content Dict 包括了当前输出的一个元素")
```

#### `tool_eval` 函数输入输出规范

- 组件的核心实现，需要添加 `@components_run_stream_trace` 装饰器，实现对组件的trace。

##### `tool_eval` 函数 输入参数

* 组件tool_eval方法的输入，除了在manifest中约定的参数外，也可能会传入以下系统变量，辅助组件的运行。
* 系统入参列表中的字段是保留字段，组件定义的manifest不能与系统参数重名。系统参数中有可以被用户设置的参数例如uploaded_files，也有不能设置的字段例如traceid等。
* 在组件的开发中，以下系统输入字段体现为 def tool_eval(self, key1, key2, \*\*kwargs)中\*\*kwargs包含的内容，key1和key2是manifest中约定的参数，kwargs中的内容是系统入参。

##### `tool_eval` 函数 组件返回字段

* 组件返回参数统一采用json字段，固定key名称和对应的value，value默认是dict类型，value本身需要指定visible_scope。
* 非流式返回结果，按照所有流式内容的key-value进行合并，例如两个event都是references，那么需要两组references合并，所有组件需要支持非流式返回。
* 基于sse协议提供流式数据
* content 本身是个 List[Dict]，每个 Dict是当前 event 的一个元素，一般有多个元素的返回例如 urls/files 才需要多个 Dict

###### 组件返回字段总览

|字段|类型|是否必须|默认值 及 取值范围|作用说明|备注|
|---|---|---|---|---|---|
|role|str|否|- tool 默认<br>- user<br>- assistant<br>|ole是区分当前消息来源的重要字段，对于绝大多数组件而言，都是填写tool，标明role所在的消息来源为组件。部分思考及问答组件，role需要填写为assistant|{"role": "tool"}|
|content|list[dict]|是|[]Event|当前组件返回内容的主要payload，List[Dict]，每个 Dict 包括了当前 event 的一个元素||
|+ name|str|否|part1，part2或者3d_pics，title|介绍当前yield内容的step name使用name的必要条件，是有不同content需要是属于结构上的不同字段，但又是streaming的||
|+ type|str|是|* text 默认<br>* code<br>* files<br>* urls<br>* oral_text<br>* references<br>* image<br>* chart<br>* audio<br>* json|代表event 类型，包括 text、code、files、urls、oral_text、references、image、chart、audio、tought、json<br>该字段的取值决定了下面text字段的内容结构||
|+ text|dict<br>object|是|{}|代表当前 event 元素的内容，每一种 event 对应的 text 结构固定|保留字段<br>"text": {'filename': 'chart_url.png', 'url': 'https://chart_url.png'},|
|+ visible_scope|str|否|all 默认<br>llm<br>user<br>空|为了界面展示明确的说明字段<br>* llm为思考模型可见，类似function calling结果中submit的执行结果<br>* user为终端用户可见|workflow中存在消息通知节点，类型为notice<br>目前实测，llm、user、all用户都可见，只是气泡不一样。llm在下拉框中，user直接输出到气泡中。|
|+ raw_data|dict<br>object|否|{}|内部信息，由开发者请求透传，内部系统返回的信息，例如API节点收到的resp，大模型节点的MB resp|{<br>    "origin_response": "xxxxx"<br>}|
|+ usage|list of dict<br>object|否|{}|大模型的token用量|{<br>    "prompt_tokens": 1547,<br>    "completion_tokens": 2,<br>    "total_tokens": 1549,<br>    "name": "ERNIE Speed-AppBuilder"<br>}|
|+ metrics|dict<br>object|否|{}|耗时、性能、内存等trace及debug所需信息|{<br>    "begin_timestamp": xxxxx<br>    "end_timestamp": xxxxx<br>}|

##### 包含 `manifests` 定义的 `tool_eval` 函数返回示例

```python
class SimilarQuestion(CompletionBaseComponent):
    r""" 
    基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
    
    Examples:

    .. code-block:: python
        
        import os
        import appbuilder

        os.environ["APPBUILDER_TOKEN"] = "..."

        qa_mining = appbuilder.SimilarQuestion(model="Qianfan-Agent-Speed-8k")

        msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        msg = appbuilder.Message(msg)
        answer = qa_mining(msg)

        print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    manifests = [
        {
            "name": "similar_question",
            "description": "基于输入的问题，挖掘出与该问题相关的类似问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "输入的问题，用于大模型根据该问题输出相关的类似问题。"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    def __init__(
            self,
            model: str="Qianfan-Agent-Speed-8K",
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = True,
    ):
        """初始化StyleRewrite模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
            SimilarQuestionMeta, model=model, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)

    @components_run_stream_trace
    def tool_eval(self, 
                  query: str,
                  **kwargs):
        """
        根据给定的query和可选参数生成并返回文本输出。
        
        Args:
            query (str): 需要生成文本的输入查询字符串。
            **kwargs: 其他可选参数。
        
        Returns:
            Generator[Output]: 返回一个生成器，生成类型为Output的对象。
        
        """
        traceid = kwargs.get("_sys_traceid")
        msg = Message(query)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, stream=False, temperature=temperature, top_p=top_p, request_id=traceid)
        
        yield self.create_output(type="text", text=str(message.content), name="text", usage=message.token_usage)
```

## 代码合入单元测试规范

## 注释规范