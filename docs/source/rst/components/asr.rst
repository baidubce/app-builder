
短语音识别-极速版 (Automatic Speech Recognition)
================================================

简介
----

短语音识别（ASR）可以将音频流实时识别为文字，并返回每句话的开始和结束时间，适用于手机语音输入、语音搜索、人机对话等语音交互场景。

基本用法
--------

下面是短语音识别的代码示例：

.. code-block:: python

   import os
   import appbuilder
   # 设置环境变量和初始化
   os.environ["APPBUILDER_TOKEN"] = "..."

   asr = appbuilder.ASR()

   with open("./asr_test.pcm", "rb") as f:
       audio_data = f.read()
   content_data = {"audio_format": "pcm", "raw_audio": audio_data, "rate": 16000}
   msg = appbuilder.Message(content_data)
   result = asr.run(msg)

   print(result)

参数说明
--------

初始化参数
^^^^^^^^^^

无

调用参数
^^^^^^^^


* ``run``\ 函数中包含以下参数：

  * `message`: 输入的消息，用于模型的主要输入内容。这是一个必需的参数，例如：Message(content={"raw_audio": b"..."})
  * ``audio_format``\ : 定义语言文件的格式，包括"pcm"、"wav"、"amr"、"m4a"，默认值为"pcm"。
  * ``rate``\ : 定义录音采样率，固定值16000
  * ``timeout``\ : HTTP超时时间
  * ``retry``\ : HTTP重试次数

返回值示例：eg: {"result": ["北京科技馆。"]}

高级用法
--------

目前该模块仅提供基础的语音识别功能。

更新记录和贡献
--------------


* 短语音识别能力 (2023-12)
