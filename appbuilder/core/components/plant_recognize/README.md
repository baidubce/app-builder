# 植物识别（PlantRecognition）

## 简介
植物识别（PlantRecognition），即对于输入的一张图片（可正常解码，且长宽比较合适），输出植物识别结果。

### 功能介绍


### 特色优势


### 应用场景



## 基本用法

下面是植物识别的代码示例：
```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
image_url = "https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2188d971ca547c53d01742af4a2cbe"

# 从BOS存储读取样例文件
raw_image = requests.get(image_url).content
inp = appbuilder.Message(content={"raw_image": raw_image})
# inp = Message(content={"url": image_url})

# 运行植物识别
plant_recognize = appbuilder.PlantRecognition()
out = plant_recognize.run(inp)
# 打印识别结果
print(out.content)  

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
|参数名称 |参数类型 | 是否必须 | 描述                                                                    |示例值|
|--------|--------|------|-----------------------------------------------------------------------|------|
|message |String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数，例如：Message(content={"raw_image": b"..."}) |eg.示例值|
|timeout|Integer| 否    | HTTP超时时间                                                              |10|
|retry|Integer| 否    | HTTP重试次数                                                              |3|

### 响应参数
|参数名称 | 参数类型  |描述 | 示例值                                              |
|--------|-------|----|--------------------------------------------------|
|plant_score_list  | list  |返回结果| [{'name': '榕树', 'score': 0.4230029582977295}...] |
### 响应示例
```json
{
  "plant_score_list": [
    {
      "name": "榕树",
      "score": 0.4230029582977295
    },
    {
      "name": "榆树",
      "score": 0.1273619383573532
    },
    {
      "name": "美国榆",
      "score": 0.1206519496
    },
    {
      "name": "白蜡树",
      "score": 0.11650644987821579
    },
    {
      "name": "雨树",
      "score": 0.045340824872255325
    }
  ]
}
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的植物识别。

