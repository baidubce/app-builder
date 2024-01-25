# 图像内容理解 （ImageUnderstand）

## 简介
图像内容理解 （ImageUnderstand），为丰富AI应用工作台接入的PaaS能力，与VIS沟通新增图像理解能力，会基于输入的图片、问题、prompt，输出理解图片后的文本信息。同时，支持客户自主选择，是否调用大模型对输出文本进行润色，目前支持百度文心大模型调用。
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
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 
os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数

无

### 调用参数
| 参数名称       | 参数类型   | 是否必须 | 描述                          |示例值|
|------------|--------|------|-----------------------------|---|
| message    | String | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数 ||
| +content   | Dict   | 是    | 消息内容                        ||
| +raw_image | String | 否    | 原始图片字节流                     ||
| +url       | String   | 否    | 图片下载链接地址                    ||
| +question  | String   | 是    | 问题字符串，长度小于100               ||
|timeout|Integer| 否    | HTTP超时时间                    |10||
|retry|Integer| 否    | HTTP重试次数                    |3||

### 响应参数
| 参数名称      | 参数类型 | 描述     | 示例值                                             |
|-----------|------|--------|-------------------------------------------------|
|  description | String  | 图像理解内容 | "用户上传的图像，经过前期模型分析存在以下信息：;;整个图像内容"                                                |

### 响应示例
```json
{
	"description": "用户上传的图像，经过前期模型分析存在以下信息：;;整个图像内容可以表述为：...，回答如下问题：图片里内容是什么?, 注意不要复述提供的资料内容"
}
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的图像内容理解。

## 更新记录和贡献
* 图像内容理解 (2024-01)