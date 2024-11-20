# appbuilder.core.components.tree_mind package

## Submodules

## appbuilder.core.components.tree_mind.component module

树图工具

### *class* appbuilder.core.components.tree_mind.component.TreeMind(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

树图工具，提供智能思维导图制作工具和丰富的模板，支持脑图、逻辑图、树形图、鱼骨图、组织架构图、时间轴、时间线等多种专业格式。
.. code-block:: python

> import os
> import requests
> import appbuilder
> # 请前往千帆AppBuilder官网创建密钥，流程详见：[https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)
> os.environ["GATEWAY_URL"] = "..."
> os.environ["APPBUILDER_TOKEN"] = "..."
> treemind = appbuilder.TreeMind()
> resp = treemind.run(appbuilder.Message("生成一份年度总结的思维导图"), to_lang="en")
> print(resp.content)
> # 输出 {'from_lang':'zh', 'to_lang':'en', 'trans_result':[{'src':'你好','dst':'hello'},{'src':'中国','dst':'China'}]}

#### manifests *= [{'description': '根据用户输入的信息，生成详细智能思维导图、脑图、逻辑图、树形图、鱼骨图、组织架构图、时间轴、时间线等多种专业格式思维导图', 'name': 'tree_mind', 'parameters': {'properties': {'query': {'description': '用户想要生成思维导图的内容', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### name *= 'tree_mind'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), \*\*kwargs) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

运行组件
:param message: 消息对象
:type message: Message

* **返回:**
  返回消息对象
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(query, \*\*kwargs)

调用树图查询接口
:param query: 用户想要生成思维导图的内容
:type query: string

* **返回:**
  返回生成的思维导图的图片链接和跳转链接
* **返回类型:**
  dict

#### version *= 'v1'*
