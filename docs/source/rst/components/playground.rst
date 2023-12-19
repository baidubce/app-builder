
空应用（Playground）
====================

简介
----

Playground空应用（Playground）是一款灵活的组件，允许用户自定义prompt模板并执行。它适用于各种场景，特别是在需要自定义输入模板和使用预训练模型进行交互的情况下。

Playground 组件使用手册
=======================

简介
----

Playground 是一个灵活的组件，允许用户自定义prompt模板并执行。它适用于各种场景，特别是在需要自定义输入模板和使用预训练模型进行交互的情况下。

基本用法
--------

要开始使用 Playground，你需要设置prompt模板和模型名称。以下是一个基本示例：

.. code-block:: python

   import os
   import appbuilder

   os.environ["APPBUILDER_TOKEN"] = "..."

   play = appbuilder.Playground(
       prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。",
       model="ernie-bot-4"
   )
   play(appbuilder.Message({"name": "小明", "bot_name": "小红", "bot_type": "聊天机器人", "bot_function": "聊天", "bot_question": "你好吗？"}), stream=False)

参数说明
--------

初始化参数
^^^^^^^^^^


* ``prompt_template`` (str): 输入模板，用于指定prompt格式。
* ``model`` (str|None): 模型名称，用于指定要使用的千帆模型。

调用参数
^^^^^^^^


* ``message`` (obj:\ ``Message``\ ): 输入消息，必需参数。
* ``stream`` (bool, 可选): 是否以流式形式返回响应，默认为 False。
* ``temperature`` (float, 可选): 模型配置的温度参数，默认值为 1e-10。

返回值
^^^^^^


* obj:\ ``Message``\ : 模型运行后的输出消息。

高级用法
--------

此部分可根据实际应用场景提供更复杂的示例和用法说明。

示例和案例研究
--------------

目前暂无具体案例，将在未来更新。

API文档
-------

无

更新记录和贡献
--------------


* 初始版本发布。
* 如您希望为空模板组件贡献代码或反馈，请参考 `贡献指南 <#>`_\ 。
