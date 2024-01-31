# 菜品识别（DishRecognition）

## 简介
菜品识别组件（DishRecognition）可以识别超过9千种菜品，可准确识别图片中的菜品名称、卡路里，适用于多种客户识别菜品的业务场景中。

### 功能介绍
识别超过9千种菜品，适用于识别只含有单个菜品的图片，接口返回菜品的名称、卡路里等综合信息

### 特色优势
识别精度高，响应速度快

### 应用场景
1. 餐饮健康：根据拍摄照片，识别图片中菜品名称，获取菜品参考卡路里含量和百科信息，可结合识别结果进一步提供饮食推荐、健康管理方案等相关功能，增强用户体验，广泛应用于餐饮娱乐类和健康管理类APP中
2. 智能结算：根据拍摄照片，识别图片中菜品名称和位置，提高结算效率，减少人工录入成本，广泛应用于餐饮行业中

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

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
无

### 调用参数
|参数名称 |参数类型 |是否必须 |描述 | 示例值    |
|--------|--------|--------|----|--------|
|message |obj:`Message`  |是 |待识别的图片字节流数据或url| Message(content={"raw_image": b"..."}) 或Message(content={"url": "..."}) |
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
|retry|Integer|否 |HTTP重试次数| 3      |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |List[Object]  |返回结果|[{"name": "剁椒鱼头", "calorie": "127"}]|
|result[0].name    |String  |菜品名称|剁椒鱼头|
|result[0].calorie |String  |菜品卡路里含量|127|


### 响应示例
```json
{"result": [{"name": "剁椒鱼头", "calorie": "127"}]}
```

### 错误码
|错误码|描述|
|------|---|

## 更新记录和贡献
* 菜品识别 (2024-01)