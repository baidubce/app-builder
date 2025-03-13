# 通用文字识别-高精度版（GeneralOCR）

## 简介

通用文字识别组件（GeneralOCR）支持多场景、多语种、高精度的文字识别服务，对图片全部文字内容进行检测识别。

### 功能介绍
覆盖多种通用场景、20+种语言的高精度整图文字检测和识别服务，包括各类印刷和手写文档、网络图片、表格、印章、数字、二维码等；

### 特色优势
* 准确率高

    多项ICDAR指标居世界第一，识别准确率高
### 应用场景
支持多场景、多语种、高精度的文字识别服务，可用于纸质文档电子化、办公文档/报表识别、图像内容审核等场景
## 基本用法

以下是一个简单的例子来演示如何开始使用GeneralOCR组件：

示例图片为![示例图片](https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae857a27513734d765495f89ffa5f73)

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
image_base64 = base64.b64encode(raw_image)
general_ocr = appbuilder.GeneralOCR()
out = general_ocr.run(appbuilder.Message(content={"image_base64": image_base64}))
print(out.content)
```

##  参数说明

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
| message | Message  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数 | Message(content={"image_base64": "待识别的图片base64数据", "image_url": ...}), 优先级image_base64 > image_url > pdf_base64 > pdf_url |
| +image_base64 | String | 否 | 待识别的图片base64数据, 要求base64编码和urlencode后大小不超过10M，最短边至少15px，最长边最大8192px，支持jpg/jpeg/png/bmp格式 | 略 |
| +image_url | String | 否 | 待识别的图片url, 要求base64编码和urlencode后大小不超过10M，最短边至少15px，最长边最大8192px，支持jpg/jpeg/png/bmp格式 | "https://bj.bcebos.com/agi-dev-platform-sdk-test/1.png" |
| +pdf_base64 | String | 否 | 待识别的pdf文件base64数据，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过10M，最短边至少15px，最长边最大8192px，支持jpg/jpeg/png/bmp格式 | 略 |
| +pdf_url | String | 否 | 待识别的pdf文件url，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过10M，最短边至少15px，最长边最大8192px，支持jpg/jpeg/png/bmp格式 | "https://bj.bcebos.com/agi-dev-platform-sdk-test/8、质量流量计.pdf" |
| +pdf_file_num | String | 否 | 需要识别的PDF文件的对应页码，当 pdf_file 参数有效时，识别传入页码的对应页面内容，若不传入，则默认识别第 1 页 | "1" |
| +detect_direction | String | 否 | 是否检测图像朝向，默认不检测，即：false。朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括: true-检测朝向, false：不检测朝向 | "false" |
| +multidirectional_recognize | String | 否 | 是否开启行级别的多方向文字识别，可选值包括: true-识别, false-不识别.若图内有不同方向的文字时，建议将此参数设置为“true” | "true" |
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
| retry   | Integer | 否    | HTTP重试次数                    | 3                                              |

### 响应参数
| 参数名称         | 参数类型    | 描述      | 示例值                                               |
|--------------|---------|---------|---------------------------------------------------|
| words_result | Array[] | 返回结果    | [{"words":"一站式企业级大模型平台，提供先进的生成式AI生产及应用全流程开发工具链"}] |
| + words      | String  | 识别结果字符串 | "百度智能云千帆大模型平台"                                    |

### 响应示例
```json
{
    "words_result":[
        {
            "words":"一站式企业级大模型平台，提供先进的生成式AI生产及应用全流程开发工具链"
        },
        {
            "words":"百度智能云千帆大模型平台"
        },
        {
            "words":"文心大模型4.0已正式发布，个人和企业客户可通过百度智能云千帆大模型平台接入使用"
        },
        {
            "words":"立即使用"
        },
        {
            "words":"在线体验"
        },
        {
            "words":"使用文档"
        },
        {
            "words":"定价说明"
        },
        {
            "words":"千帆社区"
        },
        {
            "words":"常见概念、使用指导"
        },
        {
            "words":"定价、计费方式、计量说明"
        },
        {
            "words":"大模型开发学习、交流社区"
        }
    ]
}
```

## 高级用法

目前该模块仅提供基础通用文字识别功能。


## 更新记录和贡献
* 通用文字识别能力 (2023-12)
* 增加Pdf格式输入，增加detect_direction和multidirectional_recognize入参
