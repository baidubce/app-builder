# 通用文字识别-高精度版（GeneralOCR）

## 简介

通用文字识别组件（GeneralOCR）支持多场景、多语种、高精度的文字识别服务，对图片/文件全部文字内容进行检测识别。

### 功能介绍
覆盖多种通用场景、20+种语言的高精度整图文字检测和识别服务，包括各类印刷和手写文档、网络图片、表格、印章、数字、二维码等；

### 特色优势
* 准确率高

    针对图片模糊、倾斜、翻转等情况进行专项优化，鲁棒性强，多项ICDAR指标居世界第一，识别准确率高
### 应用场景
支持多场景、多语种、高精度的文字识别服务，可用于纸质文档电子化、办公文档/报表识别、图像内容审核等场景
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

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
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
| timeout | Integer | 否    | HTTP超时时间                    | 10                                             |
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
### 错误码
| 错误码 | 描述 |
|-----|----|

## 高级用法

目前该模块仅提供基础通用文字识别功能。


## 更新记录和贡献
* 通用文字识别能力 (2023-12)
