# AgentBuilder组件

## 简介

AgentBuilder组件支持调用Console端已发布智能体应用的会话能力

### 功能介绍

具体包括创建会话、上传文档、运行对话等

### 特色优势

与云端Console AgentBuilder能力打通，实现低代码会话

### 应用场景

快速、高效集成云端已发布智能体应用能力

## 基本用法

以下是使用SDK进行问答的示例代码

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AgentBuilder应用ID，可在console端查看
# 初始化智能体
agent = appbuilder.AgentBuilder(app_id)
# 创建会话
conversation_id = agent.create_conversation()
# 运行对话
out = agent.run("北京天气怎么样", conversation_id)
# 打印会话结果 
print(out.content.answer)
```

## 参数说明

### 鉴权说明

使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。

```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

- `app_id`: 线上AgentBuilder应用ID，可在[console](https://console.bce.baidu.com/ai_apaas/app)上查看和获取，示例如图

<img width="768" alt="image" src="./image/agentbuilder.png">

### 调用参数

| 参数名称            | 参数类型         | 是否必须 | 描述         | 示例值        |
|-----------------|--------------|------|------------|------------|
| conversation_id | String       | 是    | 会话ID       |            |
| query           | String       | 否    | query问题内容  | "今天天气怎么样?" |
| file_ids        | list[String] | 否    | 对话可引用的文档ID | False      |
| stream          | Bool         | 否    | 是否流式返回     | False      |

### 非流式返回

| 参数名称           | 参数类型               | 描述               | 示例值                                                                    |
|----------------|--------------------|------------------|------------------------------------------------------------------------|
| content        | AgentBuilderAnswer | 对话返回结果           |                                                                        |
| +code          | Int                | 错误码,0代码成功，非0表示失败 | 0                                                                      |
| +message       | String             | 错误具体消息           |                                                                        |
| +answer        | String             | 智能体返回的回答         |                                                                        |
| +events        | List[Event]        | 事件列表             |                                                                        |
| +events[0]     | Event              | 具体事件内容           |                                                                        |
| ++code         | String             | 错误码              |                                                                        |
| ++message      | String             | 错误具体消息           |                                                                        |
| ++status       | String             | 事件状态             | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）                 |
| ++event_type   | String             | 事件类型             |                                                                        |
| ++content_type | String             | 内容类型             | 可选值包括：code text, image, status,image, function_call, rag, audio、video等 |
| ++detail       | Dict               | 事件输出详情           | 代码解释器、文生图、工具组件等的详细输出内容                                                 |

### 流式返回

| 参数名称    | 参数类型             | 描述                             | 示例值 |
|---------|------------------|--------------------------------|-----|
| content | Python Generator | 可迭代，每次迭代返回AgentBuilderAnswer类型 | 无   |

### 响应示例

```
Message(name=msg, content=北京市的面积是16410.54平方公里^[2]^。, mtype=dict, extra={'search_baidu': [{'id': '1', 'content': '北京,简称“京”,是中华人民共和国的首都,是全国的政治中心、文化中心,是世界著名古都和现代化国际...', 'type': 'web', 'from': 'search_baidu', 'title': '北京概况_首都之窗_北京市人民政府门户网站', 'url': 'https://www.beijing.gov.cn/renwen/bjgk/?eqid=b987a5f000085b6700000002642e204d'}, 'id', 'content', 'type', 'from', 'title', 'url']}, conversation_id=5a247540-e8cf-402a-a630-8015c24904f5)
```

## 高级用法

```python

import appbuilder
from appbuilder.core.console.agent_builder.model import *
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AgentBuilder应用ID，可在console端查看
# 初始化智能体
agent = appbuilder.AgentBuilder(app_id)
# 创建会话
conversation_id = agent.create_conversation()

# 上传一个介绍介绍北京旅游景点的文档
file_id = agent.upload_local_file(conversation_id, "/path/to/pdf/file")
# 开始对话，引用上传的文档
message = agent.run(conversation_id, "北京天气怎么样", file_ids=[file_id, ], stream=True)

# 打印会话结果 
answer = ""

# 每次迭代返回AgentBuilderAnswer结构，内可能包括多个事件内容
for content in message.content:
    # 流式场景下，answer内容流式返回，需要将每次返回的answer拼接起来才是完整的对话结果
    answer += content.answer
    for event in content.events:
        content_type = event.content_type
        detail = event.detail
        # 根据content类型对事件详情进行解析
        if content_type == "code":
            code_detail = CodeDetail(**detail)
            print(code_detail.code)
        elif content_type == "text":
            text_detail = TextDetail(**detail)
            print(text_detail.text)
        elif content_type == "image":
            image_detail = ImageDetail(**detail)
            print(image_detail.url)
        elif content_type == "rag":
            rag_detail = RAGDetail(**detail)
            print(rag_detail.references)
        elif content_type == "function_call":
            function_call_detail = FunctionCallDetail(**detail)
            print(function_call_detail.video)
        elif content_type == "audio":
            audio_detail = AudioDetail(**detail)
            print(audio_detail)
        elif content_type == "video":
            video_detail = VideoDetail(**detail)
            print(video_detail)
        elif content_type == "status":
            StatusDetail(**detail)
    else:
        print(detail)
print(answer)
```

## 更新记录和贡献
* 集成Console AgentBuilder能力(2024-03)