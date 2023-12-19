
地标识别（LandmarkRecognition）
===============================

简介
----

地标识别组件（LandmarkRecognition）可以识别12万中外著名地标、热门景点，可返回地标名称。

基本用法
--------

.. code-block:: python

   import os
   import appbuilder

   os.environ["APPBUILDER_TOKEN"] = '...'
   # 使用with语句以读取文件方式打开文件，并获取文件字节流
   with open("xxxx.jpg", "rb") as f:
       # 输入参数为一张图片
       inp = appbuilder.Message(content={"raw_image": f.read()})
       # 进行地标识别
       landmark_recognize = appbuilder.LandmarkRecognition()
       out = landmark_recognize.run(inp)
       # 打印识别结果
       print(out.content) # for example: {"landmark": "狮身人面相"}

参数说明
--------

组件不需要初始化参数。

参数说明
^^^^^^^^

run函数接收的参数定义：


* message (Message, 必选): 输入图片或图片url下载地址用于执行识别操作。例如：Message(content={"raw_image": b"..."}) 或 Message(content={"url": "https://image/download/url"})
* timeout (float, 可选): HTTP超时时间。
* retry (int, 可选): HTTP重试次数。

返回的message定义：


* (Message): 模型识别结果。例如： Message(content={"landmark": b"狮身人面相"})

高级用法
--------

该组件同时支持通过传入图片的URL地址进行地标识别

.. code-block:: python


   import appbuilder

   # 输入参数为图片的url
   inp = appbuilder.Message(content={"url": "https://image/download/url"})
   landmark_recognize = appbuilder.LandmarkRecognition()

   # 进行地标识别
   out = landmark_recognize.run(inp)
   # 打印识别结果
   print(out.content) # for example: {"landmark": "狮身人面相"}
