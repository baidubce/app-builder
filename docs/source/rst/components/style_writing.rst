
风格写作（StyleWriting）
========================

简介
----

风格写作组件（StyleWriting）是一款基于生成式大模型进行文本创作的工具，支持多种风格，包括B站、小红书等，适用于编写文案、广告等多种场景。

基本用法
--------

为了快速开始使用风格写作组件，您可以参考以下步骤：

.. code-block:: python

   import appbuilder
   import os

   os.environ["APPBUILDER_TOKEN"] = "..."

   model = "eb-turbo-appbuilder"
   style_writing = appbuilder.StyleWriting(model)

   query = "帮我写一篇关于人体工学椅的文案"
   style = "小红书"
   length = 100

   msg = appbuilder.Message(query)
   answer = style_writing(msg, style, length)

参数说明
--------

初始化参数
^^^^^^^^^^


* ``model``\ : 模型名称，用于指定要使用的千帆模型。

调用参数
^^^^^^^^


* ``message (Message)``\ : 主要输入内容，例如“帮我生成一个介绍保温杯的话术”。这是一个必需参数。
* ``style_query (str)``\ : 风格查询选项，可选择 'B站', '小红书', '通用'。默认为 '通用'。
* ``length (int)``\ : 输出内容的长度，可选 '短' (100), '中' (300), '长' (600)。默认为 100。
* ``stream (bool)``\ : 是否以流式形式返回响应。默认为 False。
* ``temperature (float)``\ : 模型的生成概率调整参数。范围为 0.0 到 1.0，默认为 1e-10。

返回值
^^^^^^


* 返回一个 ``Message`` 对象，包含模型运行后的输出消息。

高级用法
--------

使用风格写作组件进行更复杂的文本创作，例如调整不同的风格和长度参数来适应特定的写作场景。

示例和案例研究
--------------

目前暂无具体的实际应用案例。

API文档
-------

更多详细信息，请访问 `风格写作组件API文档 <#>`_\ 。

更新记录和贡献
--------------


* 初始版本发布。
* 如您希望为风格写作组件贡献代码或反馈，请参考 `贡献指南 <#>`_\ 。
