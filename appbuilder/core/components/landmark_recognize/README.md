# 地标识别（LandmarkRecognition）

## 简介
地标识别组件（LandmarkRecognition）可以识别12万中外著名地标、热门景点，可返回地标名称。

### 功能介绍


### 特色优势


### 应用场景



## 基本用法

下面是地标识别的代码示例：
```python
import os

import requests

import appbuilder

#  请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
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
|timeout|Integer| 否    | HTTP超时时间                    |10||
|retry|Integer| 否    | HTTP重试次数                    |3||

### 响应参数
| 参数名称     | 参数类型 | 描述   | 示例值    |
|----------|------|------|--------|
| landmark | str  | 地标名字 | 比如：尼罗河 |
### 响应示例
```json
{"landmark": "尼罗河"}
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的地标识别。

## 更新记录和贡献
* 地标识别 (2024-01)