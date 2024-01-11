# 菜品识别（DishRecognition）

## 简介
菜品识别组件（DishRecognition）可以识别超过9千种菜品，可准确识别图片中的菜品名称、卡路里，适用于多种客户识别菜品的业务场景中。


## 基本用法
通过如下示例代码可以快速开始使用菜品识别组件：

```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

dish_recognition = appbuilder.DishRecognition()

image_url = "https://bj.bcebos.com/v1/appbuilder/dish_recognize_test.jpg?" \
          "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T" \
          "10%3A58%3A25Z%2F-1%2Fhost%2F7b8fc08b2be5adfaeaa4e3a0bb0d1a1281b10da" \
          "3d6b798e116cce3e37feb3438"
raw_image = requests.get(image_url).content

resp = dish_recognition(appbuilder.Message({"raw_image": raw_image}))
# 输出{'result': [{'name': '剁椒鱼头', 'calorie': '127'}]}
print(resp.content)
```
其中，`APPBUILDER_TOKEN`为您的API访问授权token。

## 参数说明

### 初始化参数

该组件在初始化时无需任何参数。

### 调用参数说明

`DishRecognition` 组件的 `run` 方法接受以下参数：

- `message`(Message) - 输入待识别图片，必传参数，支持传图片二进制流和图片URL。
- `timeout`(float) - 请求超时时间，可选参数，默认为 None。
- `retry`(int) - 重试次数，可选参数，默认为 0。

该方法返回一个 `Message` 对象，该对象中的 `content` 值是一个字典，包含菜品识别结果。例如，`Message(content={'result': [{'name': '剁椒鱼头', 'calorie': '127'}]})`。