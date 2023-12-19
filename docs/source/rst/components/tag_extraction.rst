
标签抽取（TagExtraction）
=========================

简介
----

标签抽取组件（TagExtraction）是一款高效的标签抽取组件，基于生成式大模型，专门用于从文本中提取关键标签。它适用于各种文本分析场景，如内容分类、关键词提取等。

基本用法
--------

要开始使用 ``TagExtraction``\ ，首先需要设置环境变量 ``APPBUILDER_TOKEN``\ ，然后创建 ``TagExtraction`` 实例并传递文本消息。

.. code-block:: python

   import os
   import appbuilder

   os.environ["APPBUILDER_TOKEN"] = '...'

   tag_extraction = appbuilder.TagExtraction(model="ernie-bot-4")
   result = tag_extraction(appbuilder.Message("从这段文本中抽取关键标签"))

这个例子展示了如何实例化 ``TagExtraction`` 组件并使用一个文本消息进行标签抽取。

参数说明
--------

初始化参数
^^^^^^^^^^


* ``model`` (str|None): 模型名称，用于指定要使用的千帆模型。

调用参数
^^^^^^^^


* ``message`` (obj:\ ``Message``\ ，必选): 输入消息，为模型提供主要的输入内容。
* ``stream`` (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
* ``temperature`` (float, 可选): 模型配置的温度参数，用于调整生成概率。取值范围为 0.0 到 1.0。

返回值:


* ``obj:Message``\ : 模型运行后的输出消息，包含抽取的标签信息。

高级用法
--------

高级用法可以包括自定义模型参数或使用不同的模型源。例如，可以通过指定不同的 ``model`` 来使用特定于域的模型进行标签抽取。

.. code-block:: python

   tag_extraction = appbuilder.TagExtraction(model="custom-model")
   result = tag_extraction(appbuilder.Message("自定义模型抽取的标签"))

示例和案例研究
--------------

在实际应用中，\ ``TagExtraction`` 可以用于新闻文章、社交媒体帖子或其他任何文本内容的关键标签提取，帮助内容创建者或营销分析师快速了解主要主题和趋势。

API文档
-------

更详细的API文档，请参考 `AppBuilder TagExtraction API Documentation <#>`_.

更新记录和贡献
--------------


* v1.0: 初始版本，提供基本的标签抽取功能。
  如果您有兴趣贡献代码或提供反馈，请访问 `GitHub repository <#>`_\ 。
