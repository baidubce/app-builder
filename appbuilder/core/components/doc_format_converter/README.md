# 文档格式转换 (DocFormatConverter)

## 简介
文档格式转换：识别文档内文字及版面布局，可将多种类型的版式文档转换为流式文档。

### 功能介绍
支持识别图片/PDF文档版面布局，提取文字内容，并转换为保留原文档版式的Word/Excel，方便二次编辑和复制。

### 特色优势
1、多种格式互转：支持多种格式相互转换，覆盖全面；

2、图像预处理：支持对文件朝向检测、印章/水印去除后等预处理，提升格式转换效果。

### 应用场景
文档电子化：标题/正文/表格/配图等版式信息精准识别与还原，快速录入文档内容，实现纸质档案电子化。

## 基本用法


```python
import os
import requests
import appbuilder


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

doc_format_converter = appbuilder.DocFormatConverter()

image_url = "https://ai-cape-strategy-data.bj.bcebos.com/document-restructure/1EF33F9307451C9413D5D1160.jpg"

resp = doc_format_converter(appbuilder.Message({"file_path": image_url}))
# 输出{"word_url":"", "excel_url":""}
print(resp.content)
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
| 参数名称       |参数类型 |是否必须 | 描述          | 示例值  |
|------------|--------|--------|-------------|------|
| file_path    |String  |是 | 需要转换的文件的本地存储路径或远程URL,支持图片和PDF, URL长度不超过1024字节，图片base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/jpeg/png/bmp格式, URL对应的PDFbase64编码后大小不超过10M | "./test.pdf" |
| page_num |String|否 | 需要识别的PDF文件的对应页码，若不传入，默认识别文件所有页，页码从1开始 | '1' |


### 响应参数
| 参数名称        |参数类型 | 描述   | 示例值                     |
|-------------|--------|------|-------------------------|
| word_url |Message  | 还原后的word文件的下载地址,文件识别失败时返回" | "http://bos.bce.cn/dsfkjc.docx"|
| excel_url |Message  | 还原后的Excel文件的下载地址(源文件中含表格时才会输出),若文档中没有表格则返回"" | "http://bos.bce.cn/dsfkjc.xlsx"|

### 常见错误信息
| 错误信息                  | 描述          |
|-------------------------|-------------|
|IAM Certification failed  |IAM鉴权失败|
|Check file failed!|文件检查错误,请检查文件大小以及URL是否符合要求  |

## 更新记录和贡献
* 文档格式转换 (2024-04)