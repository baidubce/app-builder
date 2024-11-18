# 长文档内容理解（DocumentUnderstanding）

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

import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
APPBUILDER_TOKEN = "YOUR-TOKEN"
os.environ["APPBUILDER_TOKEN"] = APPBUILDER_TOKEN
du = appbuilder.DocumentUnderstanding()
query = appbuilder.Message("这篇文档讲了什么")
instruction = "请根据文档内容回答问题，用一句话简短概括"
addition_instruction = "用一句话简短概括" ##用户增强指令，可选填，该内容会进一步增强大模型的指令跟随能力，将你最需要增强效果的指令填于此，内容可以与上述的"instruction"基础指令有重复，注意：该字段内容过多会一定程度影响大模型内容严谨度，请注意控制该字段的指令字数
app_id = "YOUR-APP-ID" ##你需要在系统上自己的账号下（https://qianfan.cloud.baidu.com/appbuilder）创建任意空Agent，并获取该Agent的app_id（即界面上的应用ID，在首页->个人空间->应用 里面即会显示应用ID），这里任意空Agent就可以，无需任何配置信息，这个agent的作用只是为了获取app_id信息
file_path = "YOUR-FILE-PATH" ##填写你的本地待分析文件路径
stream = False ##是否开启流式输出功能
response_ = du.run(query, 
                   file_path, 
                   instruction=instruction, 
                   addition_instruction=addition_instruction, 
                   app_id=app_id,
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

| 参数名称                   | 参数类型 | 是否必须 | 描述                                                                       | 示例值                         |
|------------------------|------|------|--------------------------------------------------------------------------|-----------------------------|
| `message`              | obj  | 是    | 输入消息，用户输入query。                                                          | Message(content=input_data) |
| `file_path`            | str  | 是    | 用户需要分析的文档                                                                | "test.pdf"                  |
| `app_id`               | str  | 是    | 你需要在系统上自己的账号下（https://qianfan.cloud.baidu.com/appbuilder）创建任意空Agent，并获取该Agent的app_id（即界面上的应用ID，在首页->个人空间->应用 里面即会显示应用ID），这里任意空Agent就可以，无需任何配置信息，这个agent的作用只是为了获取app_id信息 | "YOUR-APP-ID"               |
| `instruction`          | str  | 否    | 用户指令                                                                     | "你的回答要严谨客观，且答案一定要分点阐述"      |
| `addition_instruction` | str  | 否    | 用户增强指令，可选填，该内容会进一步增强大模型的指令跟随能力，将你最需要增强效果的指令填于此，注意：该字段内容过多会一定程度影响大模型内容严谨度 | "你的答案需要分点阐述"                |

### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- |------| -------- | -------- |
| `result` | str  | 模型运行后的输出结果 | "" |

### 响应示例-流式输出
```
data: {"type": "text", "text": "文件解析完成, 耗时13485.63ms\n\n"} request_id: f99a7230-649f-4170-ade7-62d8368a18e6
data: {"type": "text", "text": "**Human", "event_status": "running"} request_id: f99a7230-649f-4170-ade7-62d8368a18e6
data: {"type": "text", "text": "-Timescale Adaptation in an Open-Ended Task Space** 文档详细介绍了DeepMind团队开发的自适应代理（Adaptive Agent，简称", "event_status": "running"} request_id: f99a7230-649f-4170-ade7-62d8368a18e6
data: {"type": "text", "text": "AdA）在开放任务空间中的快速适应能力。", "event_status": "running"} request_id: f99a7230-649f-4170-ade7-62d8368a18e6
data: {"type": "text", "text": "", "event_status": "done"} request_id: f99a7230-649f-4170-ade7-62d8368a18e6
```

### 响应示例-非流式输出
```
{'code': 0, 'message': '', 'result': {'text': '文件解析完成, 耗时14572.57ms\n\n**Human-Timescale Adaptation in an Open-Ended Task Space** 文档详细介绍了DeepMind团队开发的自适应代理（Adaptive Agent，简称AdA）在开放任务空间中的快速适应能力。以下是文档的主要内容和贡献点：\n\n1. **引言**：\n   - 强调了快速适应能力对于人工智能的重要性，特别是在现实世界中的应用和与人类互动的场景中。\n   - 提出了通过元强化学习（meta-RL）和自动课程学习（auto-curriculum learning）等方法，训练能够在未见过的环境中快速适应的代理。\n\n2. **自适应代理（AdA）**：\n   - 介绍了AdA的设计和训练方法，包括其在开放任务空间中的适应行为、记忆架构、以及如何通过自动课程学习来优化训练过程。\n   - 展示了AdA能够在几分钟内解决复杂的3D任务，且不需要进一步的代理训练，显示了其快速适应的能力。\n\n3. **实验与结果**：\n   - 在多个方面评估了AdA的性能，包括其在单代理和多代理设置下的适应能力、不同架构和课程学习方法的影响、以及模型大小和记忆长度对性能的影响。\n   - 通过与人类玩家的比较，证明了AdA在适应速度上与人类相当。\n\n4. **相关工作**：\n   - 回顾了与本工作相关的领域，包括程序化环境生成、开放任务学习、适应性和强化学习中的Transformer应用等。\n\n5. **结论**：\n   - 总结了AdA的贡献，强调了其在开放任务空间中快速适应的能力，以及通过元强化学习和自动课程学习等方法训练大型模型的可能性。\n\n6. **作者和贡献**：\n   - 列出了主要贡献者和部分贡献者，以及项目的赞助商和认可。\n\n**主要贡献点**：\n- 提出了AdA，一个能够在开放任务空间中快速适应的代理，其适应速度与人类相当。\n- 通过元强化学习和自动课程学习等方法，训练了大型Transformer模型，展示了其在开放任务空间中的快速适应能力。\n- 分析了不同架构、课程学习方法、模型大小和记忆长度对AdA性能的影响，提供了详细的实验结果和比较。\n- 通过与人类玩家的比较，证明了AdA在适应速度上的优势。'}, 'request_id': '687642b0-b877-49ed-9ad9-65d76de0ea58'}
```

## 高级用法

## 更新记录和贡献
### 2024.10. 15
#### [Added]
- 第一版