# AgentBuilder组件

## 简介

AgentBuilder组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)
平台上通过AgentBuilder构建并发布的智能体应用。

### 功能介绍

具体包括创建会话、上传文档、运行对话等

### 特色优势

与云端Console AgentBuilder能力打通，实现低代码会话

### 应用场景

快速、高效集成云端已发布智能体应用能力

## 基本用法

### Python

#### 组件初始化参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| app_id | string | 线上RAG应用的ID | "正确的应用ID" |

#### Run方法入参

| 参数名称            | 参数类型         | 是否必须 | 描述                                                 | 示例值        |
|-----------------|--------------|------|----------------------------------------------------|------------|
| conversation_id | String       | 是    | 会话ID                                               |            |
| query           | String       | 否    | query问题内容                                          | "今天天气怎么样?" |
| file_ids        | list[String] | 否    | 对话可引用的文档ID                                         |            |
| stream          | Bool         | 否    | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 | False      |

#### Run方法非流式返回

| 参数名称           | 参数类型               | 描述         | 示例值                                                                    |
|----------------|--------------------|------------|------------------------------------------------------------------------|
| content        | AgentBuilderAnswer | 对话返回结果     |                                                                        |
| +answer        | String             | 智能体应用返回的回答 |                                                                        |
| +events        | List[Event]        | 事件列表       |                                                                        |
| +events[0]     | Event              | 具体事件内容     |                                                                        |
| ++code         | String             | 错误码        |                                                                        |
| ++message      | String             | 错误具体消息     |                                                                        |
| ++status       | String             | 事件状态       | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）                 |
| ++event_type   | String             | 事件类型       |                                                                        |
| ++content_type | String             | 内容类型       | 可选值包括：code text, image, status,image, function_call, rag, audio、video等 |
| ++detail       | Dict               | 事件输出详情     | 代码解释器、文生图、工具组件、RAG等的详细输出内容                                             |

#### Run方法流式返回

| 参数名称    | 参数类型             | 描述                             | 示例值 |
|---------|------------------|--------------------------------|-----|
| content | Python Generator | 可迭代，每次迭代返回AgentBuilderAnswer类型 | 无   |

#### 非流式调用示例

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
out = agent.run(conversation_id, "北京今天天气怎么样")
# 打印会话结果 
print(out.content.answer)
```

#### 流式调用示例

```python

import appbuilder
from appbuilder.core.console.agent_builder import data_class
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AgentBuilder应用的ID
# 初始化智能体
agent = appbuilder.AgentBuilder(app_id)
# 创建会话
conversation_id = agent.create_conversation()

# 上传一个介绍某汽车产品的说明文档
file_id = agent.upload_local_file(conversation_id, "/path/to/pdf/file")
# 引用上传的文档，开始对话
message = agent.run(conversation_id, "汽车性能参数怎么样", file_ids=[file_id, ], stream=True)

answer = ""

# 每次迭代返回AgentBuilderAnswer结构，内可能包括多个事件内容
for content in message.content:
    # stream=True时，将answer拼接起来才是完整的的对话结果
    answer += content.answer
    for event in content.events:
        content_type = event.content_type
        detail = event.detail
        # 根据content类型对事件详情进行解析
        if content_type == "code":
            code_detail = data_class.CodeDetail(**detail)
            print(code_detail.code)
        elif content_type == "text":
            text_detail = data_class.TextDetail(**detail)
            print(text_detail.text)
        elif content_type == "image":
            image_detail = data_class.ImageDetail(**detail)
            print(image_detail.url)
        elif content_type == "rag":
            rag_detail = data_class.RAGDetail(**detail)
            print(rag_detail.references)
        elif content_type == "function_call":
            function_call_detail = data_class.FunctionCallDetail(**detail)
            print(function_call_detail.video)
        elif content_type == "audio":
            audio_detail = data_class.AudioDetail(**detail)
            print(audio_detail)
        elif content_type == "video":
            video_detail = data_class.VideoDetail(**detail)
            print(video_detail)
        elif content_type == "status":
            status_detail = data_class.StatusDetail(**detail)
            print(status_detail)
        else:
            default_detail = data_class.DefaultDetail(**detail)
            print(default_detail)

# 打印完整的answer结果
print(answer)
```

### Java

### Go

#### 组件初始化参数

| 参数名称   | 参数类型      | 描述         | 示例值       |
|--------|-----------|------------|-----------|
| app_id | string    | 线上RAG应用的ID | "正确的应用ID" |
| config | SDKConfig | SDK配置信息    |           |

#### Run方法入参

| 参数名称           | 参数类型         | 是否必须 | 描述                                                 | 示例值         |
|----------------|--------------|------|----------------------------------------------------|-------------|
| conversationID | 会话ID         | 是    | 若为空字符串服务端会自动创建新的会话ID，若不为空则继续上次对话内容                 |             |
| query          | string       | 是    | query内容                                            | "汽车性能参数怎么样" |
| stream         | bool         | 是    | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |             |
| file_ids       | list[String] | 否    | 对话可引用的文档ID                                         |             |

#### Run方法出参

| 参数名称                 | 参数类型                 | 描述                   | 示例值 |
|----------------------|----------------------|----------------------|-----|
| AgentBuilderIterator | AgentBuilderIterator | 回答迭代器，流式/非流式均统一返回该类型 |     |
| error                | error                | 存在错误时error不为nil，反之   |     |

#### 迭代AgentBuilderIterator

| 参数名称          | 参数类型        | 描述         | 示例值                                                                    |
|---------------|-------------|------------|------------------------------------------------------------------------|
| +Answer       | string      | 智能体应用返回的回答 |                                                                        |
| +Events       | []Event     | 事件列表       |                                                                        |
| +Events[0]    | Event       | 具体事件内容     |                                                                        |
| ++Code        | string      | 错误码        |                                                                        |
| ++Message     | string      | 错误具体消息     |                                                                        |
| ++Status      | string      | 事件状态       | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）                 |
| ++EventType   | string      | 事件类型       |                                                                        |
| ++ContentType | string      | 内容类型       | 可选值包括：code text, image, status,image, function_call, rag, audio、video等 |
| ++Detail      | interface{} | 事件输出详情     | 代码解释器、文生图、工具组件、RAG等的详细输出内容                                             |

#### 示例代码

```Go
package main

import (
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://appbuilder.baidu.com
	os.Setenv("GATEWAY_URL", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	agentBuilder, err := appbuilder.NewAgentBuilder(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := agentBuilder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}
	// 与创建AgentBuilder应用时绑定的知识库不同之处在于，
	// 所上传文件仅在本次会话ID下发生作用，如果创建新的会话ID，上传的文件自动失效
	// 而知识库在不同的会话ID下均有效
	fileID, err := agentBuilder.UploadLocalFile(conversationID, "/path/to/cv.pdf")
	if err != nil {
		fmt.Println("upload local file failed:", err)
		return
	}
	// 执行流式对话
	i, err := agentBuilder.Run(conversationID, "描述简历中的候选人情况", []string{fileID}, true)
	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}

	completedAnswer := ""
	var answer *appbuilder.AgentBuilderAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		completedAnswer = completedAnswer + answer.Answer
		for _, ev := range answer.Events {
			if ev.ContentType == appbuilder.TextContentType {
				detail := ev.Detail.(appbuilder.TextDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.CodeContentType {
				detail := ev.Detail.(appbuilder.CodeDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.ImageContentType {
				detail := ev.Detail.(appbuilder.ImageDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.RAGContentType {
				detail := ev.Detail.(appbuilder.RAGDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.FunctionCallContentType {
				detail := ev.Detail.(appbuilder.FunctionCallDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.AudioContentType {
				detail := ev.Detail.(appbuilder.AudioDetail)
				fmt.Println(detail.Audio)
			} else if ev.ContentType == appbuilder.VideoContentType {
				detail := ev.Detail.(appbuilder.VideoDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.StatusContentType {
			} else { // 默认detail
				detail := ev.Detail.(appbuilder.DefaultDetail)
				fmt.Println(detail)
			}
		}
	}
	// 迭代正常结束err应为io.EOF
	if errors.Is(err, io.EOF) {
		fmt.Println("run success")
		fmt.Println("智能体回答内容： ", completedAnswer)
	} else {
		fmt.Println("run failed:", err)
	}
}
```
