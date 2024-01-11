# 通用物体和场景识别-高级版（ObjectRecognition）

## 简介
通用物体和场景识别组件（ObjectRecognition）可以识别超过10万类常见物体和场景，接口返回大类及细分类的名称。广泛适用于图像或视频内容分析、拍照识图等业务场景。
## 基本用法

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
```

## 参数说明

* run函数:
    * message (`Message`类型): 图片或图片url下载地址, 用于执行识别操作。例如: `Message(content={"raw_image": b"..."})` 或 `Message(content={"url": "https://image/download/url"})`.
    * timeout (float类型, 可选): HTTP请求的超时时间。
    * retry (int类型, 可选): HTTP请求的重试次数。
   返回值:
    * message (`Message`类型): 模型识别结果。例如: `Message(content={"result":[{"keyword":"苹果","score":0.94553,"root":"植物-蔷薇科"},{"keyword":"姬娜果","score":0.730442,"root":"植物-其它"},{"keyword":"红富士","score":0.505194,"root":"植物-其它"}]})`

## 高级用法
目前该模块仅提供基础通用物体与场景识别功能。

## 更新记录和贡献
* 通用物体及场景识别 (2023-12-08)