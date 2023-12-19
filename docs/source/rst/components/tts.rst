
短文本在线合成（TTS）
=====================

简介
----

短文本在线合成组件（TTS）提供高度拟人、流畅自然的语音合成服务，将文本朗读出来，基础音库性价比更高，精品音库听感更逼真。

基本用法
--------

下面是一个简单的例子来指导你开始使用这个组件

.. code-block:: python

   import os
   import appbuilder

   os.environ["APPBUILDER_TOKEN"] = '...'
   tts = appbuilder.TTS()

   # 使用baidu-tts模型, 默认返回MP3格式
   inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
   out = tts.run(inp)
   with open("sample.mp3", "wb") as f:
       f.write(out.content["audio_binary"])

   # 使用paddlespeech-tts模型，目前只支持返回WAV格式
   inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
   out = tts.run(inp, model="paddlespeech-tts", audio_type="wav")
   with open("sample.wav", "wb") as f:
       f.write(out.content["audio_binary"])

参数说明
--------

参数说明
^^^^^^^^

run 函数接收的参数定义:


* message (obj: ``Message``\ ): 待转为语音的文本. 举例: Message(content={"text": "欢迎使用百度语音"})
* 如果选择\ ``baidu-tts``\ 模型，\ ``text``\ 最大文本长度为1024 GBK编码长度, 如果选择\ ``paddlespeech-tts``\ 模型, ``text``\ 最大文本长度是510个字符.
* model (str, 可选): 默认是\ ``baidu-tts``\ 模型，可设置为\ ``paddlespeech-tts``
* speed(int, 可选): 语音语速，默认是5中等语速，取值范围在0~15之间，如果选择模型为paddlespeech-tts，参数自动失效
* pitch(int, 可选): 语音音调，默认是5中等音调，取值范围在0~15之间，如果选择模型为paddlespeech-tts，参数自动失效
* volume(int, 音量): 语音音量，默认是5中等音量，取值范围在0~15之间，如果选择模型为paddlespeech-tts，参数自动失效
* person(int, 可选): 语音人物特征，默认是0,可选值包括度小宇=1 度小美=0 度逍遥（基础）=3 度丫丫=4 度逍遥（精品）=5003
* 度小鹿=5118 度博文=106 度小童=110 度小萌=111 度米朵=103 度小娇=5，如果选择模型为paddlespeech-tts，参数自动失效
* audio_type(str, 可选): 音频文件格式，默认是\ ``mp3``\ , 如果选择\ ``paddlespeech-tts``\ 模型，参数只能设为\ ``wav``
* timeout (float, 可选): HTTP超时时间
* retry (int, 可选)： HTTP重试次数

返回参数说明:


* message (obj: ``Message``\ ): 文本转语音结果. 举例: Message(content={"audio_binary": b"xxx", "audio_type": "mp3"})
