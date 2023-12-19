# 菜品识别（DishRecognition）

## 简介
菜品识别组件（DishRecognition）可以识别超过9千种菜品，可准确识别图片中的菜品名称、卡路里，适用于多种客户识别菜品的业务场景中。


## 基本用法
通过如下示例代码可以快速开始使用菜品识别组件：

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

dish_recognition = appbuilder.DishRecognition()

with open("xxxx.jpg", "rb") as f:
    resp = dish_recognition(appbuilder.Message({"raw_image": f.read()}))
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