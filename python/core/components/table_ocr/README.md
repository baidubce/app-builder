# 表格文字识别 (TableOCR) 

## 简介
表格文字识别 (TableOCR) 可支持识别图片中的表格内容，返回各表格的表头表尾内容、单元格文字内容及其行列位置信息，全面覆盖各类表格样式，包括常规有线表格、无线表格、含合并单元格表格。同时，支持多表格内容识别。
### 功能介绍
* 简单表格文字识别

支持识别具备完整框线的常规简单表格，结构化输出表头、表尾及每个单元格的文字内容。
* 复杂表格文字识别

可识别无表格框线，但行、列位置明确的表格，支持含合并单元格的复杂表格文字识别。
### 特色优势
* 支持识别图片中的表格内容，返回各表格的表头表尾内容、单元格文字内容及其行列位置信息，全面覆盖各类表格样式，包括常规有线表格、无线表格、含合并单元格表格。同时，支持单图中多表格内容的识别。

### 应用场景
* 信息登记表识别

  对个人、商品、公示内容等纸质信息登记表进行识别，用于登记信息的结构化整理和统计，大幅度降低人力录入成本，提升信息管理的便捷性
* 财税报表识别

  提取识别银行对账单、资产负债表、损益表等财税场景常用表格内容，快速实现表格内容的电子化，用于财税信息统计、存档及核算，大幅度提升信息录入效率
## 基本用法

下面是表格文字识别的代码示例：

示例图片为

![示例图片](https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6064079145ff4698856f477b820147768fc2187d3)

```python
import os
import appbuilder
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

# 从BOS读取样例图片
image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024" \
            "-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
            "064079145ff4698856f477b820147768fc2187d3"
raw_image = requests.get(image_url).content
# 创建表格文字识别组件实例
table_ocr = appbuilder.TableOCR()
# 执行识别操作并获取结果
out = table_ocr.run(appbuilder.Message(content={"raw_image": raw_image}))
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

### 调用参数 （以表格形式展示）
| 参数名称    | 参数类型    | 是否必须 | 描述                          | 示例值                                            |
|---------|---------|------|-----------------------------|------------------------------------------------|
| message | String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数 | Message(content={"raw_image": b"待识别的图片字节流数据"}) |
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
| retry   | Integer | 否    | HTTP重试次数                    | 3                                              |

### 响应参数
| 参数名称             | 参数类型    | 描述            | 示例值                                                                                                                                                                                      |
|------------------|---------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tables_result    | array[] | 返回结果          | [{"table_location": [],"header": [],"body": [],"footer": []}]                                                                                                                            |
| +table_location	 | array[] | 单个表格的四角点x,y坐标 | [{ "x": 15, "y": 15 },{ "x": 371, "y": 15 },{ "x": 371, "y": 98 },{ "x": 15, "y": 98 }],                                                                                                 |
| +header          | array[] | 表头信息          | [{'location': [{'x': 325, 'y': 40}, {'x': 528, 'y': 40}, {'x': 528, 'y': 71}, {'x': 325, 'y': 71}], 'words': '财务状况变动表'}, {...}]                                                          |
| +body	           | array[] | 单元格信息         | [{"cell_location": [{ "x": 15, "y": 15 },{ "x": 120, "y": 15 },{ "x": 120, "y": 58 },{ "x": 15, "y": 58 }],"row_start": 0,"row_end": 1,"col_start": 0,"col_end": 1,"words": "参数"},{...}] |
| +footer	         | array[] | 表尾信息          | [{'location': [...], 'words': '...'}, {...}]                                                                                                                                             |

### 响应示例
```json
{
  "tables_result": [
    {
      "table_location": [
        { "x": 15, "y": 15 },
        { "x": 371, "y": 15 },
        { "x": 371, "y": 98 },
        { "x": 15, "y": 98 }
      ],
      "header": [],
      "body": [
        {
          "cell_location": [
            { "x": 15, "y": 15 },
            { "x": 120, "y": 15 },
            { "x": 120, "y": 58 },
            { "x": 15, "y": 58 }
          ],
          "row_start": 0,
          "row_end": 1,
          "col_start": 0,
          "col_end": 1,
          "words": "参数"
        },
        {
          "cell_location": [
            { "x": 120, "y": 15 },
            { "x": 371, "y": 15 },
            { "x": 371, "y": 58 },
            { "x": 120, "y": 58 }
          ],
          "row_start": 0,
          "row_end": 1,
          "col_start": 1,
          "col_end": 2,
          "words": "值"
        },
        {
          "cell_location": [
            { "x": 15, "y": 58 },
            { "x": 120, "y": 58 },
            { "x": 120, "y": 98 },
            { "x": 15, "y": 98 }
          ],
          "row_start": 1,
          "row_end": 2,
          "col_start": 0,
          "col_end": 1,
          "words": "Content-Type"
        },
        {
          "cell_location": [
            { "x": 120, "y": 58 },
            { "x": 371, "y": 58 },
            { "x": 371, "y": 98 },
            { "x": 120, "y": 98 }
          ],
          "row_start": 1,
          "row_end": 2,
          "col_start": 1,
          "col_end": 2,
          "words": "application/x-www-form-urlencoded"
        }
      ],
      "footer": []
    }
  ]
}
```
### 错误码
| 错误码 | 描述 |
|-----|----|

## 高级用法

目前该模块仅提供基础的表格文字识别功能。


## 更新记录和贡献
* 表格文字识别能力 (2024-01)