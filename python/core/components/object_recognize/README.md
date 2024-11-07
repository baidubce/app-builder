# 通用物体和场景识别-高级版（ObjectRecognition）

## 简介
通用物体和场景识别组件（ObjectRecognition）可以识别超过10万类常见物体和场景，接口返回大类及细分类的名称。广泛适用于图像或视频内容分析、拍照识图等业务场景。
### 功能介绍
* 识别物体或场景名称

  识别动物、植物、商品、建筑、风景、动漫、食材、公众人物等10万个常见物体及场景，接口返回大类及细分类的名称结果；

### 特色优势
* 可识别超过10万类常见物体和场景，接口返回大类及细分类的名称，并支持获取识别结果对应的百科信息；

### 应用场景
可以识别超过10万类常见物体和场景，广泛适用于图像或视频内容分析、拍照识图等业务场景


## 基本用法

示例图片为：

![示例图片](https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc1ba1de0a8f072bc5a87102bd32f9e3)



```python
import os
import appbuilder
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

# 从BOS读取样例图片
image_url = "https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?"\
    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-"\
    "11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc"\
    "1ba1de0a8f072bc5a87102bd32f9e3"
raw_image = requests.get(image_url).content
# 创建物体识别组件实例
object_recognition = appbuilder.ObjectRecognition()
# 执行识别操作并获取结果
out = object_recognition.run(appbuilder.Message(content={"raw_image": raw_image}))
print(out.content)
# {'result': [{'keyword': '苹果', 'score': 0.961247, 'root': '植物-蔷薇科'}, {'keyword': '姬娜果', 'score': 0.740838, 'root': '植物-其它'}, {'keyword': '梨子', 'score': 0.392218, 'root': '商品-水果'}, {'keyword': '车厘子', 'score': 0.193986, 'root': '植物-其它'}, {'keyword': '石榴', 'score': 0.000239, 'root': '植物-千屈菜科'}]}
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

### 调用参数 （以表格形式展示）
| 参数名称    | 参数类型    | 是否必须 | 描述                          | 示例值                                            |
|---------|---------|------|-----------------------------|------------------------------------------------|
| message | String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数 | Message(content={"raw_image": b"待识别的图片字节流数据"}) |
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
| retry   | Integer | 否    | HTTP重试次数                    | 3                                              |

### 响应参数
| 参数名称     | 参数类型    | 描述          | 示例值                                                 |
|----------|---------|-------------|-----------------------------------------------------|
| result   | Array[] | 返回结果        | [{"keyword":"苹果","score":0.961247,"root":"植物-蔷薇科"}] |
| +keyword | String  | 图片中的物体或场景名称 | "苹果"                                                |
| +score	  | Float   | 置信度         | 0.961247                                            |
| +root	   | String  | 识别结果的上层标签   | "植物-蔷薇科"                                            |


### 响应示例
```json
{
    "result":[
        {
            "keyword":"苹果",
            "score":0.961247,
            "root":"植物-蔷薇科"
        },
        {
            "keyword":"姬娜果",
            "score":0.740838,
            "root":"植物-其它"
        },
        {
            "keyword":"梨子",
            "score":0.392218,
            "root":"商品-水果"
        },
        {
            "keyword":"车厘子",
            "score":0.193986,
            "root":"植物-其它"
        },
        {
            "keyword":"石榴",
            "score":0.000239,
            "root":"植物-千屈菜科"
        }
    ]
}
```
### 错误码
| 错误码 | 描述 |
|-----|----|

## 高级用法
目前该模块仅提供基础通用物体与场景识别功能。

## 更新记录和贡献
* 通用物体及场景识别 (2023-12-08)
