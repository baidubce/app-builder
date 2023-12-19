# 通用物体和场景识别-高级版（ObjectRecognition）

## 简介
通用物体和场景识别组件（ObjectRecognition）可以识别超过10万类常见物体和场景，接口返回大类及细分类的名称。广泛适用于图像或视频内容分析、拍照识图等业务场景。
## 基本用法

```python
import os
import appbuilder


# 配置token环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 打开需要识别的图像文件
with open("./object_recognition_test.jepg", "rb") as f:
    # 创建物体识别组件实例
    object_recognition = appbuilder.ObjectRecognition()
    # 执行识别操作并获取结果
    out = object_recognition.run(appbuilder.Message(content={"raw_image": f.read()}))
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