# 文件生成PPT（PPTGenerationFromFile）

## 简介
长文档内容理解组件（DocumentUnderstanding）支持对图片以及文档内容进行理解，并基于图片以及文档内容对用户的提问进行回答，
包括但不限于文档内容问答、总结摘要、内容分析。
### 功能介绍
根据用户上传的文档（支持txt、docx、pdf、xlsx、png、jpg、jpeg等多种格式）、query、指令生成大模型答案
### 特色优势
处理长上下文的大模型内容理解任务
### 应用场景
长上下文的文档问答

## 基本用法
### 快速开始

```python

import uuid
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
APPBUILDER_TOKEN = "YOUR-TOKEN"
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
uid = str(uuid.uuid4())
trace_id = str(uuid.uuid4()) 
conversation_id = str(uuid.uuid4()) ## 注意你的conversation_id不能和之前的请求重复，不然会直接返回之前已有的conversation_id的答案
du = appbuilder.DocumentUnderstanding()
query = appbuilder.Message("这篇文档讲了什么")
instruction = "请根据文档内容回答问题"
addition_instruction = "请你用一句话简短概括" ##用户增强指令，可选填，该内容会进一步增强大模型的指令跟随能力，将你最需要增强效果的指令填于此，内容可以与上述的"instruction"基础指令有重复，注意：该字段内容过多会一定程度影响大模型内容严谨度，请注意控制该字段的指令字数
file_path = "YOUR-FILE-PATH" ##填写你的本地待分析文件路径
stream = False ##是否开启流式输出功能
response_ = du.run(query, 
                   file_path, 
                   instruction=instruction, 
                   addition_instruction=addition_instruction, 
                   uid=uid,
                   trace_id=trace_id, 
                   conversation_id=conversation_id, 
                   stream=stream)

for result in response_:
    print(result) ##打印输出的大模型答案
```


## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
import os
os.environ['APPBUILDER_TOKEN'] = 'bce-YOURTOKEN'
```


### 初始化参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `secret_key` | str | 否 | 用户鉴权token，默认从环境变量中获取: `os.getenv("APPBUILDER_TOKEN", "")` | bce-v3/XXX |
| `gateway` | str | 否 | 后端网关服务地址，默认从环境变量中获取: `os.getenv("GATEWAY_URL", "")` | https://appbuilder.baidu.com |
| `lazy_certification` | bool | 否 | 延迟认证，为True时在第一次运行时认证。默认为False。 | False |


### 调用参数

| 参数名称                   | 参数类型 | 是否必须 | 描述                                                                       | 示例值             |
|------------------------|------|------|--------------------------------------------------------------------------|-----------------|
| `message`              | obj  | 是    | 输入消息，用户输入query。                                                          | Message(content=input_data) |
| `file_path`            | str  | 是    | 用户需要分析的文档                                                                | "test.pdf"      |
| `instruction`          | str  | 否    | 用户指令                                                                     | "你的回答要严谨客观"     |
| `addition_instruction` | str  | 否    | 用户增强指令，可选填，该内容会进一步增强大模型的指令跟随能力，将你最需要增强效果的指令填于此，注意：该字段内容过多会一定程度影响大模型内容严谨度 | "你的答案需要分点阐述"    |


### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- |------| -------- | -------- |
| `result` | str  | 模型运行后的输出结果 | "" |

### 响应示例
```
您好，请问您是想询问关于残疾人办理什么证件的问题吗？如果是，我可以为您提供一些信息。

首先，如果您是首次申请办理残疾人证，需要携带身份证、户口簿和三张两寸近期免冠白底彩色照片到县残联办证窗口提出申请。如果您因身体原因无法亲自前往，可以联系村（社区）工作人员代办申请。

其次，如果您是指残疾类型等级证明，您需要携带相关材料到指定医院或医生进行评级，并由医生签名盖章。

最后，如果您是指残疾人享受低保或残疾人贫困证的一级肢体、视力、智力、精神、多重及60周岁以上的一级听力、语言的重度残疾人可以享受重度残疾人生活补助，那么您需要携带身份证、户口本和残疾证申请表到县、市、区级残联进行办理。

希望这些信息对您有所帮助。如果您还有其他问题，欢迎随时提问。
```

## 高级用法

## 更新记录和贡献
### 2024.10. 15
#### [Added]
- 第一版