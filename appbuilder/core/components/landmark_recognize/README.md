# 地标识别（LandmarkRecognition）

## 简介

地标识别组件（LandmarkRecognition）可以识别12万中外著名地标、热门景点，可返回地标名称。

## 基本用法
```python
import os

import requests

import appbuilder

# 可前往千帆AppBuilder官网 https://console.bce.baidu.com/ai_apaas/sdk 创建密钥
os.environ["APPBUILDER_TOKEN"] = '...'
# 从BOS存储读取样例文件
image_url = "https://bj.bcebos.com/v1/appbuilder/landmark_test.jpeg?" \
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
            "11T10%3A59%3A56Z%2F-1%2Fhost%2Fc249a068c6f321b91" \
            "da0d0fd629b26ded58dcac2b6a3674f32378f5eb8df1ed0"
raw_image = requests.get(image_url).content
    # 输入参数为一张图片
inp = appbuilder.Message(content={"raw_image": raw_image})
# 进行地标识别
landmark_recognize = appbuilder.LandmarkRecognition()
out = landmark_recognize.run(inp)
# 打印识别结果
print(out.content) # eg: {"landmark": "尼罗河"}

```
## 参数说明
组件不需要初始化参数。

### 参数说明
run函数接收的参数定义：

- message (Message, 必选): 输入图片或图片url下载地址用于执行识别操作。例如：Message(content={"raw_image": b"..."}) 或 Message(content={"url": "https://image/download/url"})
- timeout (float, 可选): HTTP超时时间。
- retry (int, 可选): HTTP重试次数。

返回的message定义：

- (Message): 模型识别结果。例如： Message(content={"landmark": b"狮身人面相"})

## 高级用法
该组件同时支持通过传入图片的URL地址进行地标识别
```python

import appbuilder

# 输入参数为图片的url
inp = appbuilder.Message(content={"url": "https://image/download/url"})
landmark_recognize = appbuilder.LandmarkRecognition()

# 进行地标识别
out = landmark_recognize.run(inp)
# 打印识别结果
print(out.content) # for example: {"landmark": "狮身人面相"}
```
