# 二维码识别 (QRcodeOCR) 

## 简介
二维码识别 (QRcodeOCR) 可对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息。


### 功能介绍
* 二维码识别

    检测识别图片中的二维码（包括QR_CODE、DATA_MATRIX、AZTEC、PDF_417 4类），自动返回存储的内容。
* 条形码识别

    检测识别图片中的条形码（包括CODE_128、UPC_A、EAN_13、ITF、CODABAR 等9类），自动返回存储的内容。
### 特色优势
* 支持对图片中的二维码、条形码进行检测和识别，自动返回存储的内容。

### 应用场景
* 物品信息管理

    解析识别各类物品的二维码或条形码信息，应用于商品、药品出入库管理及货物运输管理等场景，轻松一扫即可快速完成对物品信息的读取、登记和存储，简化物品管理流程
## 基本用法

下面是二维码识别的代码示例：

示例图片为：
![示例图片](https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6e74ab057ce26d50e966dc31ff083e6a9c41b)

```python
import os
import appbuilder
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

# 从BOS读取样例图片
image_url = "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?" \
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-" \
            "01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6" \
            "e74ab057ce26d50e966dc31ff083e6a9c41b"
raw_image = requests.get(image_url).content
# 创建二维码识别组件实例
qrcode_ocr = appbuilder.QRcodeOCR()
# 执行识别操作并获取结果
out = qrcode_ocr.run(appbuilder.Message(content={"raw_image": raw_image}), location="true")
print(out.content)
# {'codes_result': [{'type': 'QR_CODE', 'text': ['ocr文字识别'], 'location': {'top': 506, 'left': 1302, 'width': 1972, 'height': 1961}}]}
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
| 参数名称     | 参数类型    | 是否必须 | 描述                                                                      | 示例值                                            |
|----------|---------|------|-------------------------------------------------------------------------|------------------------------------------------|
| message  | String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数                                             | Message(content={"raw_image": b"待识别的图片字节流数据"}) |
| location | String  | 否    | 是否输出二维码/条形码位置信息，false：不返回位置信息，true：默认值，返回图中二维码/条形码的位置信息，包括上边距、左边距、宽度、高度 | "false"                                        |
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
| retry    | Integer | 否    | HTTP重试次数                                                                | 3                                              |

### 响应参数
| 参数名称         | 参数类型     | 描述          | 示例值                                                                                                               |
|--------------|----------|-------------|-------------------------------------------------------------------------------------------------------------------|
| codes_result | Array[]  | 返回结果        | [{'type': 'QR_CODE', 'text': ['ocr文字识别'], 'location': {'top': 506, 'left': 1302, 'width': 1972, 'height': 1961}}] |
| +type        | String   | 识别码类型条码类型   | 'QR_CODE'                                                                                                         |
| +text        | Array[]  | 条形码/二维码识别内容 | ['ocr文字识别']                                                                                                       |
| +location    | Object{} | 条形码/二维码位置信息 | {'top': 506, 'left': 1302, 'width': 1972, 'height': 1961}                                                         |
| ++top	       | Integer  | 条形码/二维码的上边距 | 506                                                                                                               |
| ++left       | Integer  | 条形码/二维码的左边距 | 1302                                                                                                              |
| ++width	     | Integer  | 条形码/二维码的宽度  | 1972                                                                                                              |
| ++height     | Integer  | 条形码/二维码的高度  | 1961                                                                                                              |


### 响应示例
```json
{
  "codes_result": [
    {
      "type": "QR_CODE",
      "text": ["ocr文字识别"],
      "location": {
        "top": 506,
        "left": 1302,
        "width": 1972,
        "height": 1961
      }
    }
  ]
}
```
### 错误码
| 错误码 | 描述 |
|-----|----|

## 高级用法

目前该模块仅提供基础的二维码识别功能。


## 更新记录和贡献
* 二维码识别能力 (2024-01)