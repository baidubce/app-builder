# 动物识别 (Animal Recognition) 

## 简介
动物识别 (Animal Recognition) 可用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出动物识别结果。

### 功能介绍
* 识别动物名称

  识别近八千种动物，接口返回动物名称、置信度信息，支持自定义返回结果数；

### 特色优势
* 可识别近八千种动物，接口返回动物名称，并可获取识别结果对应的百科信息；

### 应用场景
* 拍照识图

    根据拍摄照片，识别图片中动物的名称，可配合其它识图能力对识别的结果进一步细化，提升用户体验，广泛应用于拍照识图类APP中。


## 基本用法

下面是动物识别的代码示例：
```python
import os
import appbuilder
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

# 从BOS读取样例图片
image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
            "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
            "62cf937c03f8c5260d51c6ae"
raw_image = requests.get(image_url).content
# 创建动物识别组件实例
animal_recognition = appbuilder.AnimalRecognition()
# 执行识别操作并获取结果
out = animal_recognition.run(appbuilder.Message(content={"raw_image": raw_image}))
print(out.content)
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
无

### 调用参数
| 参数名称    | 参数类型    | 是否必须 | 描述                          | 示例值                                            |
|---------|---------|------|-----------------------------|------------------------------------------------|
| message | String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数 | Message(content={"raw_image": b"待识别的图片字节流数据"}) |
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
| retry   | Integer | 否    | HTTP重试次数                    | 3                                              |

### 响应参数
| 参数名称   | 参数类型    | 描述   | 示例值                                   |
|--------|---------|------|---------------------------------------|
| result | Array[] | 返回结果 | [{"name":"国宝大熊猫","score":"0.975161"}] |
| +name  | String  | 动物名称 | "国宝大熊猫"                               |
| +score | String  | 	置信度 | "0.975161"                            |
### 响应示例
```json
{
    "result":[
        {
            "name":"国宝大熊猫",
            "score":"0.975161"
        },
        {
            "name":"秦岭四宝",
            "score":"0.0161979"
        },
        {
            "name":"团团圆圆",
            "score":"0.00239265"
        },
        {
            "name":"圆仔",
            "score":"0.00192277"
        },
        {
            "name":"棕色大熊猫",
            "score":"0.00130296"
        },
        {
            "name":"小熊猫",
            "score":"0.000275865"
        }
    ]
}
```

### 错误码
| 错误码 | 描述 |
|-----|----|

## 高级用法

目前该模块仅提供基础的动物识别功能。


## 更新记录和贡献
* 动物识别能力 (2024-01)