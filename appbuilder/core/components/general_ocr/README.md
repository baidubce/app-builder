# 通用文字识别-高精度版（GeneralOCR）

## 简介

通用文字识别组件（GeneralOCR）支持多场景、多语种、高精度的文字识别服务，对图片/文件全部文字内容进行检测识别。
## 基本用法

以下是一个简单的例子来演示如何开始使用GeneralOCR组件：

```python
import os
import appbuilder
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'
# 从BOS读取样例图片
image_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?"\
    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-"\
    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae"\
    "857a27513734d765495f89ffa5f73"
raw_image = requests.get(image_url).content
general_ocr = appbuilder.GeneralOCR()
out = general_ocr.run(appbuilder.Message(content={"raw_image": raw_image}))
print(out.content)
```

##  参数说明

### 初始化参数

`GeneralOCR` 初始化无需参数。

### 调用参数

- `message (obj: Message)`: 输入图片或图片url下载地址用于执行识别操作. 例如: `Message(content={"raw_image": b"..."})` 或 `Message(content={"url": "https://image/download/url"})`。
- `timeout (float, 可选)`: HTTP超时时间。
- `retry (int, 可选)`: HTTP重试次数。

返回的message定义：
- (Message): 模型识别结果。例如：  Message(content={"words_result":[{"words":"100"}, {"words":"G8"}]})

## 高级用法

目前该模块仅提供基础通用文字识别功能。


## 更新记录和贡献
* 通用文字识别能力 (2023-12)
