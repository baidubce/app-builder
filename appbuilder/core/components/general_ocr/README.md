# 通用文字识别-高精度版（GeneralOCR）

## 简介

通用文字识别组件（GeneralOCR）支持多场景、多语种、高精度的文字识别服务，对图片/文件全部文字内容进行检测识别。
## 基本用法

以下是一个简单的例子来演示如何开始使用GeneralOCR组件：

```python
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

with open("./general_ocr_test.png", "rb") as f:
    general_ocr = appbuilder.GeneralOCR()
    out = general_ocr.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```
首先，我们导入appbuilder，然后使用`appbuilder.GeneralOCR()`实例化一个GeneralOCR对象。然后我们设置环境变量APPBUILDER_TOKEN。然后我们打开一个图片文件，并使用run方法进行文字识别，打印得到的识别结果。

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
