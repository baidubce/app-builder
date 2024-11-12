# 植物识别（PlantRecognition）

## 简介
植物识别（PlantRecognition），即对于输入的一张图片（可正常解码，且长宽比较合适），输出植物识别结果。

### 功能介绍
可识别超过2万种常见植物和近8千种花卉，接口返回植物的名称，并支持获取识别结果对应的百科信息

### 特色优势
还可使用EasyDL定制训练平台，定制识别植物种类

### 应用场景
适用于拍照识图、幼教科普、图像内容分析等场景

## 基本用法

下面是植物识别的代码示例：

示例图片为

![示例图片](https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2188d971ca547c53d01742af4a2cbe)

```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
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

# {'plant_score_list': [{'name': '榕树', 'score': 0.4230029582977295}, {'name': '榆树', 'score': 0.1273619383573532}, {'name': '美国榆', 'score': 0.12065108865499496}, {'name': '白蜡树', 'score': 0.11650644987821579}, {'name': '雨树', 'score': 0.045340824872255325}]}
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
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
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
|retry|Integer| 否    | HTTP重试次数                    |3||

### 响应参数
| 参数名称             | 参数类型   | 描述     | 示例值                                              |
|------------------|--------|--------|--------------------------------------------------|
| plant_score_list | List   | 植物识别列表 |  |
| name             | String | 植物名    |  |
| score            | Float  | 植物识别打分 |  |


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


## 更新记录和贡献
* 植物识别 (2024-01)