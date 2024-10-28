# appbuilder.core.components.llms.style_rewrite package

## Submodules

## appbuilder.core.components.llms.style_rewrite.component module

### *class* appbuilder.core.components.llms.style_rewrite.component.StyleRewrite(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

文本风格转写大模型组件， 基于生成式大模型对文本的风格进行改写，支持有营销、客服、直播、激励及教学五种话术。

Examples:

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

style_rewrite = appbuilder.StyleRewrite(model="ERNIE Speed-AppBuilder")
answer = style_rewrite(appbuilder.Message("文心大模型发布新版本"), style="激励话术")
```

#### manifests *= [{'description': '能够将一段文本转换成不同的风格（营销、客服、直播、激励及教学话术），同时保持原文的基本意义不变。', 'name': 'style_rewrite', 'parameters': {'properties': {'query': {'description': '需要改写的文本。', 'type': 'string'}, 'style': {'description': '想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选. 默认是营销话术。', 'enum': ['营销话术', '客服话术', '直播话术', '激励话术', '教学话术'], 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

`StyleRewriteArgs` 的别名

#### name *: str* *= 'style_rewrite'*

#### run(message, style='营销话术', stream=False, temperature=1e-10, top_p=0.0, request_id=None)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **style** (*str* *,* *optional*) – 想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选。默认为”营销话术”。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### tool_eval(name: str, streaming: bool = False, \*\*kwargs)

执行工具评估函数

* **参数:**
  * **name** (*str*) – 函数名称，本函数不使用该参数，但保留以符合某些框架的要求。
  * **streaming** (*bool* *,* *optional*) – 是否以流的形式返回结果。默认为 False，即一次性返回结果。如果设置为 True，则以生成器形式逐个返回结果。
  * **\*\*kwargs** – 

    其他参数，包含但不限于：
    traceid (str): 请求的跟踪ID，用于日志记录和跟踪。
    query (str): 待评估的文本。
    style (str, optional): 评估风格，可选值为 [‘营销话术’, ‘客服话术’, ‘直播话术’, ‘激励话术’, ‘教学话术’]。默认为 ‘营销话术’。
    model_configs (dict, optional): 模型配置参数，可选的键包括：
    > temperature (float, optional): 温度参数，用于控制生成文本的随机性。默认为 1e-10。
    > top_p (float, optional): top_p 采样参数，用于控制生成文本的多样性。默认为 0.0。
* **返回:**
  如果 streaming 为 False，则直接返回评估结果字符串。
  如果 streaming 为 True，则以生成器形式逐个返回评估结果字符串。
* **抛出:**
  **ValueError** – 如果缺少参数 ‘query’。

#### version *: str* *= 'v1'*
