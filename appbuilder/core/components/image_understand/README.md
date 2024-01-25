# 图像内容理解 （ImageUnderstand）

## 简介
手写体OCR识别 （HandwriteOCR），支持输入图片和提问信息，可对输入图片进行理解，输出对图片的一句话描述，同时可针对图片内的主体/文字等进行检测与识别，支持返回图片内多主体/文字的内容、位置等信息

### 功能介绍


### 特色优势


### 应用场景



## 基本用法

下面是手写体的代码示例：
```python
import os
import appbuilder
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."

# 从BOS存储读取样例文件
image_url = "https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bfe25c372b7e56e6"
raw_image = requests.get(image_url).content
# 输入参数为一张图片
inp = appbuilder.Message(content={"raw_image": raw_image, "question": "图片里内容是什么?"})
# 进行图像内容理解
image_understand = appbuilder.ImageUnderstand()
out = image_understand.run(inp)
# 打印识别结果
print(out.content)
# {'description': "用户上传的图像，经过前期模型分析存在以下信息：;;整个图像内容可以表述为：...，回答如下问题：图片里内容是什么?, 注意不要复述提供的资料内容"}
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 

os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数

无

### 调用参数 （以表格形式展示）
|参数名称 |参数类型 | 是否必须 | 描述                                                                                        |示例值|
|--------|--------|------|-------------------------------------------------------------------------------------------|------|
|message |String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数，例如：Message(content={"raw_image": b"...", "question":"问一个问题"}) |eg.示例值|
|timeout|Integer| 否    | HTTP超时时间                                                                                  |10|
|retry|Integer| 否    | HTTP重试次数                                                                                  |3|

### 响应参数
| 参数名称      | 参数类型 | 描述     | 示例值                                             |
|-----------|------|--------|-------------------------------------------------|
|  description | str  | 图像理解内容 | "用户上传的图像，经过前期模型分析存在以下信息：;;整个图像内容"                                                |

### 响应示例
```json
{'description': "用户上传的图像，经过前期模型分析存在以下信息：;;整个图像内容可以表述为：...，回答如下问题：图片里内容是什么?, 注意不要复述提供的资料内容"}
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的图像内容理解。

