# console端RAG操作工具(RAG)

## 简介

RAG是基于线上RAG应用的问答组件，可以使用该组件利用线上RAG应用进行问答。<br>
<span style="color:red">
⚠️本组件仅适用于2024-04-02之前创建的历史RAG应用，最新创建的AgentBuilder应用，请参考[AgentBuilder应用](agent_builder.md)
进行调用。
</span>

### 功能介绍

利用线上RAG应用进行问答

### 特色优势

与线上应用联动，利用线上RAG应用进行问答

### 应用场景

使用SDK利用线上RAG应用进行问答

## 基本用法

以下是使用SDK进行问答的示例代码

### Python

#### 组件初始化参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| app_id | string | 线上RAG应用的ID | "正确的应用ID" |

#### run方法入参

| 参数名称            | 参数类型    | 是否必须 | 描述             | 示例值                        |
|-----------------|---------|------|----------------|----------------------------|
| query           | Message | 是    | 提问的内容          | Message(content="北京的面积多大") |
| stream          | bool    | 否    | 是否流式返回，默认False | False                      |
| conversation_id | string  | 否    | 不传默认新建会话       | ""                         |

#### run方法出参

| 参数名称   | 参数类型    | 描述   | 示例值                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------|---------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| result | Message | 返回结果 | Message(name=msg, content=北京市的面积是16410.54平方公里^[2]^。, mtype=dict, extra={'search_baidu': [{'id': '1', 'content': '北京,简称“京”,是中华人民共和国的首都,是全国的政治中心、文化中心,是世界著名古都和现代化国际...', 'type': 'web', 'from': 'search_baidu', 'title': '北京概况_首都之窗_北京市人民政府门户网站', 'url': 'https://www.beijing.gov.cn/renwen/bjgk/?eqid=b987a5f000085b6700000002642e204d'}, 'id', 'content', 'type', 'from', 'title', 'url']}, conversation_id=5a247540-e8cf-402a-a630-8015c24904f5)}) |

#### 调用示例

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

app_id = '...'  # 线上RAG应用ID，可在console端查看
conversation_id = '...'  # 会话ID，可选参数，不传默认新建会话
rag_app = appbuilder.console.RAG(app_id)
query = "中国的首都在哪里"
answer = rag_app.run(appbuilder.Message(query))  # 新建会话
print(answer.content)  # 获取结果内容
conversation_id = answer.conversation_id  # 获取会话ID，可用于下次会话
print(conversation_id)
query = "它有哪些旅游景点"
answer = rag_app.run(appbuilder.Message(query), conversation_id)  # 接上次会话
print(answer.content)  # 获取结果内容
print(answer.extra)  # 获取结果来源
```

### Java

#### 组件初始化参数

| 参数名称   | 参数类型      | 描述         | 示例值       |
|--------|-----------|------------|-----------|
| appID | String    | 线上RAG应用的ID | "正确的应用ID" |

#### Run方法入参

| 参数名称           | 参数类型   | 是否必须 | 描述                                                 | 示例值         |
|----------------|--------|------|----------------------------------------------------|-------------|
| query          | string | 是    | query内容                                                 | "汽车性能参数怎么样" |
| conversationID | String   | 是    | 若为空字符串服务端会自动创建新的会话ID，若不为空则继续上次对话内容 |             |
| stream         | boolean   | 是    | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |      |

#### Run方法出参

| 参数名称        | 参数类型        | 描述                   | 示例值 |
|-------------|-------------|----------------------|-----|
| RAGIterator | RAGIterator | 回答迭代器，流式/非流式均统一返回该类型,每次迭代返回RAGResponse类型 |     |

#### 迭代RAGIterator

| 参数名称           | 参数类型            | 描述      | 示例值 |
|----------------|-----------------|---------|-----|
| code         | int          | 响应状态码 |     |
| message | String          | 响应信息    |     |
| result    | RAGResult          | 响应结果    |     |
| +answer      | String          | 回答结果    |     |
| +conversationId  | String | 会话id    |     |
| +events       | []EventContent     | 事件流   |     |
| +events[0]       | EventContent         | 具体事件     |     |
| ++eventType       | String         | 事件类型     |     |
| ++eventStatus       | String         | 事件状态     |     |
| ++outputs       | Map<String, Object>         | 事件内容     |     |

#### 示例代码
```java
class RAGDemo {
    public static void main(String[] args) throws IOException, AppBuilderServerException {
        // 填写自己的APPBUILDER_TOKEN
        System.setProperty("APPBUILDER_TOKEN", "填写秘钥");
        // 填写创建好的appId
        String appId = "填写线上创建好的appId";
        
        RAG rag = new RAG(appId);

        RAGIterator itor = rag.run("我想了解附近的房产价格，你能帮我查询吗？", "", true);
        System.out.println("输出结果：");
        // itor.hasNext()返回false时，表示流式调用结束
        while (itor.hasNext()) {
            RAGResponse response = itor.next();
            System.out.print(response.getResult().getAnswer());
        }
    }
}
```
### Go

#### 组件初始化参数

| 参数名称   | 参数类型      | 描述         | 示例值       |
|--------|-----------|------------|-----------|
| app_id | string    | 线上RAG应用的ID | "正确的应用ID" |
| config | SDKConfig | SDK配置信息    |           |

#### Run方法入参

| 参数名称           | 参数类型   | 是否必须 | 描述                                                 | 示例值         |
|----------------|--------|------|----------------------------------------------------|-------------|
| conversationID | 会话ID   | 是    | 若为空字符串服务端会自动创建新的会话ID，若不为空则继续上次对话内容                 |             |
| query          | string | 是    | query内容                                            | "汽车性能参数怎么样" |
| stream         | bool   | 是    | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |             |

#### Run方法出参

| 参数名称        | 参数类型        | 描述                   | 示例值 |
|-------------|-------------|----------------------|-----|
| RAGIterator | RAGIterator | 回答迭代器，流式/非流式均统一返回该类型 |     |
| error       | error       | 存在错误时error不为nil，反之   |     |

#### 迭代RAGIterator

| 参数名称           | 参数类型            | 描述      | 示例值 |
|----------------|-----------------|---------|-----|
| Answer         | string          | query答案 |     |
| ConversationID | string          | 会话ID    |     |
| Events         | []RAGEvent      | RAG事件流  |     |
| +Event         | string          | 事件名     |     |
| EventStatus    | string          | 事件状态    |     |
| EventType      | string          | 事件类型    |     |
| Text           | json.RawMessage | 事件内容    |     |

#### 示例代码

```go
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
	// 初始化RAG实例
	appID := "请填写正确的应用ID"
	rag, err := appbuilder.NewRAG(appID, config)
	if err != nil {
		fmt.Println("new rag instance failed:", err)
		return
	}
	// 执行流式对话
	i, err := rag.Run("", "", true)
	if err != nil {
		fmt.Println("run failed:", err)
		return
	}
	completedAnswer := ""
	// 迭代返回结果
	var answer *appbuilder.RAGAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		completedAnswer = completedAnswer + answer.Answer
	}
	// 迭代正常结束err应为io.EOF
	if errors.Is(err, io.EOF) {
		fmt.Println("run success")
		fmt.Println("RAG智能体回答内容： ", completedAnswer)
	} else {
		fmt.Println("run failed:", err)
	}
}
```

