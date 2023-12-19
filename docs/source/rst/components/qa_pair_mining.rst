
问答对挖掘（QAPairMining）
==========================

简介
----

问答对挖掘（QAPairMining）可以基于输入文本内容，快速生成多个问题及对应答案，极大提高信息提炼的效率和准确性。广泛用于在线客服、智能问答等领域。

基本用法
--------

快速开始
^^^^^^^^

.. code-block:: python

   import os
   import appbuilder

   os.environ["APPBUILDER_TOKEN"] = "..."

   qa_mining = appbuilder.QAPairMining(model="eb-turbo-appbuilder")
   # 输入文本（对此文本挖掘问答对）
   msg = '2017年，工商银行根据外部宏观环境变化，及时调整业务策略，优化资产负债结构，' + \
       '保持存贷款业务协调发展，提升资产负债配置效率。' + \
       '2018年3月末，工商银行总资产264,937.81亿元，比上年末增加4,067.38亿元.'
   msg = appbuilder.Message(msg)
   answer = qa_mining(msg)

   print(">>> Output: {}".format(answer.content))

参数说明
--------

初始化参数
^^^^^^^^^^


* ``model`` (str|None): 模型名称，用于指定要使用的千帆模型。

调用参数
^^^^^^^^


* ``message`` (obj:\ ``Message``\ ): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
* ``stream`` (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
* ``temperature`` (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

返回:


* ``Message``\ : 模型运行后的输出消息。

高级用法
--------

基于一篇文档，快速生成多个问题及对应答案，极大提高信息提炼的效率和准确性.
主要流程如下：


#. 读取本地文档，文档解析分段，获取段落；
#. 段落作为问答对挖掘的输入，挖掘问答对。 

代码样例
^^^^^^^^

.. code-block:: python

   import os

   from appbuilder.utils.logger_util import logger
   from appbuilder import Message, DocParser, DocSplitter, QAPairMining


   file_path = "xxx.pdf"

   # 设置环境变量
   os.environ["APPBUILDER_TOKEN"] = "...."

   # 解析文档
   msg = Message(file_path)
   parser = DocParser()
   parse_result = parser.run(msg)

   # 对文档进行分段落
   splitter = DocSplitter()
   split_result = splitter(parse_result)

   # 每个段落抽取问答对，并返回结果
   for doc_segment in split_result.content:
       qa_mining = QAPairMining()
       logger.info("Input: {}".format(doc_segment.content))
       answer = qa_mining(doc_segment)
       logger.info("Output: {}".format(answer.content))
       break # debug，只跑1个段落
