# AppBuilderClient组件

## 简介

AppBuilderClient组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)
平台上通过AppBuilderClient构建并发布的智能体应用。

### 功能介绍

具体包括创建会话、上传文档、运行对话等

### 特色优势

与云端Console 应用能力打通，实现低代码会话

### 应用场景

快速、高效集成云端已发布智能体应用能力

## Python基本用法


### `AppBuilderClient().__init__()`


#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| app_id | string | 线上Agent应用的ID | "正确的应用ID" |

#### 方法返回值

```AppBuilderClient```实例化对象


### `AppBuilderClient().create_conversation()-> str`
#### 方法参数
无

#### 方法返回值

 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| conversation_id | string | 会话的ID | "80c5bbee-931d-4ed9-a4ff-63e1971bd071" |


### `AppBuilderClient().upload_file(file_path: str)-> str`
#### 方法参数
| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| file_path | string | 文件路径 | "正确的文件路径" |
#### 方法返回值
| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| file_id | string | 文件ID | "80c5bbee-931d-4ed9-a4ff-63e1971bd |


### `AppBuilderClient().run() -> Message`

#### 方法参数

| 参数名称        | 参数类型         | 是否必须 | 描述                                                         | 示例值            |
| --------------- | ---------------- | -------- | ------------------------------------------------------------ | ----------------- |
| conversation_id | String           | 是       | 会话ID                                                       |                   |
| query           | String           | 否       | query问题内容                                                | "今天天气怎么样?" |
| file_ids        | list[String]     | 否       | 对话可引用的文档ID                                           |                   |
| stream          | Bool             | 否       | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 | False             |
| tools           | List[Tool]       | 否       | 一个列表，其中每个字典对应一个工具的配置                     |                   |
| tools[0]        | Tool             | 否       | 工具配置                                                     |                   |
| +type           | String           | 否       | 枚举：<br/>**file_retrieval**: 知识库检索工具能够理解文档内容，支持用户针对文档内容的问答。<br/>**code_interpreter**: 代码解释器, 代码解释器能够生成并执行代码，从而协助用户解决复杂问题，涵盖科学计算（包括普通数学计算题）、数据可视化、文件编辑处理（图片、PDF文档、视频、音频等）、文件格式转换（如WAV、MP3、text、SRT、PNG、jpg、MP4、GIF、MP3等）、数据分析&清洗&处理（文件以excel、csv格式为主）、机器学习&深度学习建模&自然语言处理等多个领域。<br/>**function**: 支持fucntion call模式调用工具 |                   |
| +function       | Function         | 否       | Function工具描述<br/>仅当**type为**`**function**` 时需要且必须填写 |                   |
| ++name          | String           | 否       | 函数名<br/>只允许数字、大小写字母和中划线和下划线，最大长度为64个字符。一次运行中唯一。 |                   |
| ++description   | String           | 否       | 工具描述                                                     |                   |
| ++parameters    | Dict             | 否       | 工具参数, json_schema格式                                    |                   |
| tool_outputs    | List[ToolOutput] | 否       | 内容为本地的工具执行结果，以自然语言/json dump str描述       |                   |
| tool_outputs[0] | ToolOutput       | 否       | 工具执行结果                                                 |                   |
| +tool_call_id   | String           | 否       | 工具调用ID                                                   |                   |
| +output         | String           | 否       | 工具输出                                                     |                   |

#### Run方法非流式返回值

Run非流式方法返回一个`Message`对象，该对象包含以下属性：

| 参数名称           | 参数类型                   | 描述         | 示例值                                                                    |
|----------------|------------------------|------------|------------------------------------------------------------------------|
| content        | AppBuilderClientAnswer | 对话返回结果     |                                                                        |
| +answer        | String                 | 智能体应用返回的回答 |                                                                        |
| +events        | List[Event]            | 事件列表       |                                                                        |
| +events[0]     | Event                  | 具体事件内容     |                                                                        |
| ++code         | String                 | 错误码        |                                                                        |
| ++message      | String                 | 错误具体消息     |                                                                        |
| ++status       | String                 | 事件状态       | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）                 |
| ++event_type   | String                 | 事件类型       |                                                                        |
| ++content_type | String                 | 内容类型       | 可选值包括：code text, image, status,image, function_call, rag, audio、video等 |
| ++detail       | Dict                   | 事件输出详情     | 代码解释器、文生图、工具组件、RAG等的详细输出内容                                             |
| ++usage        | Usage                  | 模型调用的token用量 |  Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K')                                                                     |

`AppBuilderClientAnswer`类型定义如下：
```python
class AppBuilderClientAnswer(BaseModel):
    """执行步骤的具体内容
        属性:
            answer(str): query回答内容
            events( list[Event]): 事件列表
       """
    answer: str = ""
    events: list[Event] = []
```

`Event`类型定义如下：
```python
class Event(BaseModel):
    """执行步骤的具体内容
        属性:
            code (int): 响应code码
            message (str): 错误详情
            status (str): 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）
            event_type（str）: 事件类型
            content_type（str）: 内容类型
            detail(dict): 事件详情
            usage(Usage): 大模型调用的token用量
    """
    code: int = 0
    message: str = ""
    status: str = ""
    event_type: str = ""
    content_type: str = ""
    detail: dict = {}
    usage: Optional[Usage] = None
```


#### Run方法流式返回值

| 参数名称    | 参数类型             | 描述           | 示例值 |
|---------|------------------|--------------|-----|
| content | Python Generator | 可迭代，每次迭代返回AppBuilderClientAnswer类型 | 无   |

#### 非流式调用示例

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AppBuilder应用ID，可在console端查看
# 初始化智能体
builder = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = builder.create_conversation()
# 运行对话
out = builder.run(conversation_id, "北京今天天气怎么样")
# 打印会话结果 
print(out.content.answer)
```

#### 流式调用示例

```python

import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()

# 上传一个介绍某汽车产品的说明文档
file_id = client.upload_local_file(conversation_id, "/path/to/pdf/file")
# 引用上传的文档，开始对话
# 注意file_ids不是必填项，如果不需要引用特定文档，file_ids留空即可
message = client.run(conversation_id, "汽车性能参数怎么样", file_ids=[file_id, ], stream=True)

answer = ""

# 每次迭代返回AppBuilderClientAnswer结构，内可能包括多个事件内容
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
            if len(rag_detail.references) > 0:
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

#### Run方法带ToolCall调用示例

```python
import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."
app_id = "..."  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "仅支持中国城市的天气查询，参数location为中国城市名称，其他国家城市不支持天气查询",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名，举例：北京",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location", "unit"],
            },
        },
    }
]

msg = client.run(
    conversation_id=conversation_id, query="今天北京天气怎么样？", tools=tools
)
print(msg.model_dump_json(indent=4))

event = msg.content.events[-1]

msg_2 = client.run(
    conversation_id=conversation_id,
    tool_outputs=[{"tool_call_id": event.tool_calls[-1].id, "output": "北京今天35度"}],
)
print(msg_2.model_dump_json(indent=4))
```

## Java基本用法

### ```new AppBuilderClient(appId)```

#### 方法参数

| 参数名称   | 参数类型      | 描述         | 示例值       |
|--------|-----------|------------|-----------|
| appID | String    | 线上Agent应用的ID | "正确的应用ID" | 


#### 方法返回值

```AppBuilderClient```实例化对象

### ```AppBuilderClient().createConversation()```

#### 方法参数
无

#### 方法返回值

| 参数名称   | 参数类型      | 描述         | 示例值       |
|--------|-----------|------------|-----------|
| conversationId | String    | 创建的会话ID | "正确的会话ID" | 

### ```AppBuilderClient().run()```

#### Run方法入参`AppBuilderCientRunRequest`

| 参数名称   | 参数类型  | 是否必须 | 描述    | 示例值      |
|--------|-------|------|-------|---------|
| query          | String       | 是    | query内容                                            | "汽车性能参数怎么样" |
| conversationId | String          | 是    | 对话id，可以通过createConversation()获取                |             |
| stream         | boolean       | 是    | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |     |
| tools | List[Tool] | 否 | 一个列表，其中每个字典对应一个工具的配置 | |
| tools[0] | Tool | 否 | 工具配置 | |
| +type | String | 否 | 枚举：<br/>**file_retrieval**: 知识库检索工具能够理解文档内容，支持用户针对文档内容的问答。<br/>**code_interpreter**: 代码解释器, 代码解释器能够生成并执行代码，从而协助用户解决复杂问题，涵盖科学计算（包括普通数学计算题）、数据可视化、文件编辑处理（图片、PDF文档、视频、音频等）、文件格式转换（如WAV、MP3、text、SRT、PNG、jpg、MP4、GIF、MP3等）、数据分析&清洗&处理（文件以excel、csv格式为主）、机器学习&深度学习建模&自然语言处理等多个领域。<br/>**function**: 支持fucntion call模式调用工具 | |
| +function | Function | 否 | Function工具描述<br/>仅当**type为**`**function**` 时需要且必须填写 | |
| ++name | String | 否 | 函数名<br/>只允许数字、大小写字母和中划线和下划线，最大长度为64个字符。一次运行中唯一。 | |
| ++description | String | 否 | 工具描述 | |
| ++parameters | Dict | 否 | 工具参数, json_schema格式 | |
| tool_outputs | List[ToolOutput] | 否 | 内容为本地的工具执行结果，以自然语言/json dump str描述 | |
| tool_outputs[0] | ToolOutput | 否 | 工具执行结果 | |
| +tool_call_id | String | 否 | 工具调用ID | |
| +output | String | 否 | 工具输出 | |

#### Run方法出参
| 参数名称                 | 参数类型         | 描述                   | 示例值 |
|----------------------|--------------|--------------------|-----|
| AppBuilderClientIterator | AppBuilderClientIterator | 回答迭代器，流式/非流式均统一返回该类型,每次迭代返回AppBuilderClientIterator类型 |     |

#### 迭代AppBuilderClientIterator
| 参数名称          | 参数类型        | 描述         | 示例值                                                               |
|---------------|-------------|------------|------------------------------------------------------------------------|
| +answer       | String      | 智能体应用返回的回答 |                                                                    |
| +events       | Event[]     | 事件列表       |                                                                        |
| +events[0]    | Event       | 具体事件内容     |                                                                        |
| ++code        | string      | 错误码        |                                                                        |
| ++message     | string      | 错误具体消息     |                                                                        |
| ++status      | string      | 事件状态       | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）|
| ++eventType   | string      | 事件类型       |                                                                        |
| ++contentType | string      | 内容类型       | 可选值包括：code text, image, status,image, function_call, rag, audio、video等 |
| ++detail      | Map<String, Object> | 事件输出详情     | 代码解释器、文生图、工具组件、RAG等的详细输出内容                       |
| ++usage        | Usage                  | 模型调用的token用量 |  Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K')                                                                     |


#### 示例代码

```Java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String appId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        // 填写上传文件路径
        String fileId = builder.uploadLocalFile(conversationId, "/Users/zhangxiaoyu15/PycharmProjects/app-builder/test_app_builder_client/test.pdf");
        // 输入query
        // 注意file_ids不是必填项，如果不需要引用特定文档，则将new String[]{fileId}更换为new String[]{}即可
        AppBuilderClientIterator itor = builder.run("中国四大传统节日是哪四个", conversationId, new String[]{fileId}, false);
        StringBuilder answer = new StringBuilder();
        // itor.hasNext()返回false时，表示流式调用结束
        while(itor.hasNext())
        {
            AppBuilderClientResult response = itor.next();
            answer.append(response.getAnswer());
            for (Event event : response.getEvents()) {
                switch (event.getContentType()) {
                    case "rag":
                        List<Object> references = (List<Object>)event.getDetail().get("references");
                        for (Object reference : references) {
                            ReferenceDetail ragDetail = JsonUtils.deserialize(JsonUtils.serialize(reference), ReferenceDetail.class);
                            System.out.println("-----------------------------------");
                            System.out.println("参考文献ID:"+ragDetail.getId());
                            System.out.println("参考文献内容:"+ragDetail.getContent());
                            System.out.println("来源:"+ragDetail.getFrom());
                            System.out.println("BaiduSearch链接:"+ragDetail.getUrl());
                            System.out.println("类型:"+ragDetail.getType());
                            System.out.println("文档片段ID:"+ragDetail.getSegmentId());
                            System.out.println("文档ID:"+ragDetail.getDocumentId());
                            System.out.println("文档名称:"+ragDetail.getDocumentName());
                            System.out.println("文档所属数据集ID:"+ragDetail.getDatasetId());
                            System.out.println("-----------------------------------");
                        }
                        break;
                    default:
                        // System.out.println(event);
                }
            }
        }
        System.out.print("输出：");
        System.out.println(answer);
    }
}

class ReferenceDetail {
    private int id;
    private String content;
    private String from;
    private String url;
    private String type;
    @SerializedName("segment_id")
    private String segmentId;
    @SerializedName("document_id")
    private String documentId;
    @SerializedName("document_name")
    private String documentName;
    @SerializedName("dataset_id")
    private String datasetId;
    @SerializedName("knowledgebase_id")
    private String knowledgebaseId;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getSegmentId() {
        return segmentId;
    }

    public void setSegmentId(String segmentId) {
        this.segmentId = segmentId;
    }

    public String getDocumentId() {
        return documentId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }

    public String getDocumentName() {
        return documentName;
    }

    public void setDocumentName(String documentName) {
        this.documentName = documentName;
    }

    public String getDatasetId() {
        return datasetId;
    }

    public void setDatasetId(String datasetId) {
        this.datasetId = datasetId;
    }

    public String getKnowledgebaseId() {
        return knowledgebaseId;
    }

    public void setKnowledgebaseId(String knowledgebaseId) {
        this.knowledgebaseId = knowledgebaseId;
    }

    @Override
    public String toString() {
        return "RAGReference{" +
                "id=" + id +
                ", content='" + content + '\'' +
                ", from='" + from + '\'' +
                ", url='" + url + '\'' +
                ", type='" + type + '\'' +
                ", segmentId='" + segmentId + '\'' +
                ", documentId='" + documentId + '\'' +
                ", documentName='" + documentName + '\'' +
                ", datasetId='" + datasetId + '\'' +
                ", knowledgebaseId='" + knowledgebaseId + '\'' +
                '}';
    }
}
```

#### Run方法带ToolCall调用示例

```java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String appId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
       
       	AppBuilderClientRunRequest request = new AppBuilderClientRunRequest();
        request.setAppId(appId);
        request.setConversationID(conversationId);
        request.setQuery("今天北京的天气怎么样?");
        request.setStream(false);

        String name = "get_cur_whether";
        String desc = "这是一个获得指定地点天气的工具";
        Map<String, Object> parameters = new HashMap<>();

        Map<String, Object> location = new HashMap<>();
        location.put("type", "string");
        location.put("description", "省，市名，例如：河北省");

        Map<String, Object> unit = new HashMap<>();
        unit.put("type", "string");
        List<String> enumValues = new ArrayList<>();
        enumValues.add("摄氏度");
        enumValues.add("华氏度");
        unit.put("enum", enumValues);

        Map<String, Object> properties = new HashMap<>();
        properties.put("location", location);
        properties.put("unit", unit);

        parameters.put("type", "object");
        parameters.put("properties", properties);
        List<String> required = new ArrayList<>();
        required.add("location");
        parameters.put("required", required);

        AppBuilderClientRunRequest.Tool.Function func =
                new AppBuilderClientRunRequest.Tool.Function(name, desc, parameters);
        AppBuilderClientRunRequest.Tool tool =
                new AppBuilderClientRunRequest.Tool("function", func);
        request.setTools(new AppBuilderClientRunRequest.Tool[] {tool});

        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        String ToolCallID = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            ToolCallID = result.getEvents()[0].getToolCalls()[0].getId();
            System.out.println(result);
        }

        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest();
        request2.setAppId(appId);
        request2.setConversationID(conversationId);

        AppBuilderClientRunRequest.ToolOutput output =
                new AppBuilderClientRunRequest.ToolOutput(ToolCallID, "北京今天35度");
        request2.setToolOutputs(new AppBuilderClientRunRequest.ToolOutput[] {output});
        AppBuilderClientIterator itor2 = builder.run(request2);
        assertTrue(itor2.hasNext());
        while (itor2.hasNext()) {
            AppBuilderClientResult result = itor2.next();
            System.out.println(result);
        }
    }
}

```

## Go基本用法

### ```NewAppBuilderClient()```

#### 方法参数

| 参数名称   | 参数类型      | 描述         | 示例值       |
|--------|-----------|------------|-----------|
| app_id | string    | 线上Agent应用的ID | "正确的应用ID" |
| config | SDKConfig | SDK配置信息    |           |

### ```CreateConversation()```
#### 方法入参
无
#### 方法出参
| 参数名称         | 参数类型     | 描述                   | 示例值          |
|--------------|----------|----------------------|---------------|
| conversation | str | 创建成功的对话对象，后续操作都基于该对象进行 |               |


### ```Run()```
#### Run方法入参

| 参数名称           | 参数类型         | 是否必须 | 描述                                                 | 示例值         |
|----------------|--------------|------|----------------------------------------------------|-------------|
| conversationID | string         | 是    | 对话ID，可以通过CreateConversation()获取                |             |
| query          | string       | 是    | query内容                                            | "汽车性能参数怎么样" |
| stream         | bool         | 是    | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |             |
| file_ids       | list[String] | 否    | 对话可引用的文档ID                                         |             |

#### Run方法出参

| 参数名称                 | 参数类型                 | 描述                   | 示例值 |
|----------------------|----------------------|----------------------|-----|
| AppBuilderClientIterator | AppBuilderClientIterator | 回答迭代器，流式/非流式均统一返回该类型 |     |
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
| ++Usage        | Usage                  | 模型调用的token用量 |  Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K')                                                                     |


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
	// 设置APPBUILDER_TOKEN、GATEWAY_URL_V2环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://qianfan.baidubce.com
	os.Setenv("GATEWAY_URL_V2", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	builder, err := appbuilder.NewAppBuilderClient(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := builder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}
	// 与创建应用时绑定的知识库不同之处在于，
	// 所上传文件仅在本次会话ID下发生作用，如果创建新的会话ID，上传的文件自动失效
	// 而知识库在不同的会话ID下均有效
	fileID, err := builder.UploadLocalFile(conversationID, "/path/to/cv.pdf")
	if err != nil {
		fmt.Println("upload local file failed:", err)
		return
	}
	// 执行流式对话
    // 注意file_ids不是必填项，如果不需要引用特定的文档，则将[]string{fileID}更换为nil即可
    // 同时还需要将上文的fileID, err := builder.UploadLocalFile(conversationID,  "/path/to/cv.pdf")代码
    // 更换为 _, err = client.UploadLocalFile(conversationID,  "/path/to/cv.pdf"),否则会报错
	i, err := builder.Run(conversationID, "描述简历中的候选人情况", []string{fileID}, true)
	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}

	completedAnswer := ""
	var answer *appbuilder.AppBuilderClientAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		completedAnswer = completedAnswer + answer.Answer
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
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

### ```RunWithToolCall()```

#### Run方法入参`AppBuilderClientRunRequest`

| 参数名称       | 参数类型   | 是否必须 | 描述                                                         | 示例值               |
| -------------- | ---------- | -------- | ------------------------------------------------------------ | -------------------- |
| ConversationID | string     | 是       | 对话ID，可以通过CreateConversation()获取                     |                      |
| Query          | string     | 是       | query内容                                                    | "汽车性能参数怎么样" |
| Stream         | bool       | 是       | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |                      |
| AppID          | string     | 是       | 应用ID，线上Agent应用的ID                                    |                      |
| Tools          | []Tool     | 否       | 一个列表，其中每个字典对应一个工具的配置                     |                      |
| ToolOuptus     | []ToolOupt | 否       | 内容为本地的工具执行结果，以自然语言/json dump str描述       |                      |

`Tool`、`ToolOutput`定义如下：

```go
type Tool struct {
	Type     string   `json:"type"`
	Function Function `json:"function"`
}

type Function struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	Parameters  map[string]interface{} `json:"parameters"`
}

type ToolOutput struct {
	ToolCallID string `json:"tool_call_id" description:"工具调用ID"`
	Output     string `json:"output" description:"工具输出"`
}
```

#### Run方法出参

| 参数名称                 | 参数类型                 | 描述                                    | 示例值 |
| ------------------------ | ------------------------ | --------------------------------------- | ------ |
| AppBuilderClientIterator | AppBuilderClientIterator | 回答迭代器，流式/非流式均统一返回该类型 |        |
| error                    | error                    | 存在错误时error不为nil，反之            |        |

#### 迭代AgentBuilderIterator

| 参数名称      | 参数类型    | 描述                 | 示例值                                                       |
| ------------- | ----------- | -------------------- | ------------------------------------------------------------ |
| +Answer       | string      | 智能体应用返回的回答 |                                                              |
| +Events       | []Event     | 事件列表             |                                                              |
| +Events[0]    | Event       | 具体事件内容         |                                                              |
| ++Code        | string      | 错误码               |                                                              |
| ++Message     | string      | 错误具体消息         |                                                              |
| ++Status      | string      | 事件状态             | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成） |
| ++EventType   | string      | 事件类型             |                                                              |
| ++ContentType | string      | 内容类型             | 可选值包括：code text, image, status,image, function_call, rag, audio、video等 |
| ++Detail      | interface{} | 事件输出详情         | 代码解释器、文生图、工具组件、RAG等的详细输出内容            |
| ++Usage       | Usage       | 模型调用的token用量  | Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K') |

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
	// 设置APPBUILDER_TOKEN、GATEWAY_URL_V2环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://qianfan.baidubce.com
	os.Setenv("GATEWAY_URL_V2", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	builder, err := appbuilder.NewAppBuilderClient(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := builder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}

	parameters := make(map[string]interface{})

	location := make(map[string]interface{})
	location["type"] = "string"
	location["description"] = "省，市名，例如：河北省"

	unit := make(map[string]interface{})
	unit["type"] = "string"
	unit["enum"] = []string{"摄氏度", "华氏度"}

	properties := make(map[string]interface{})
	properties["location"] = location
	properties["unit"] = unit

	parameters["type"] = "object"
	parameters["properties"] = properties
	parameters["required"] = []string{"location"}

	i, err := client.RunWithFunctionCall(appbuilder.AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: conversationID,
		Stream:         true,
		Tools: []appbuilder.Tool{
			{
				Type: "function",
				Function: appbuilder.Function{
					Name:        "get_cur_whether",
					Description: "这是一个获得指定地点天气的工具",
					Parameters:  parameters,
				},
			},
		},
	})
	if err != nil {
		fmt.Println("run failed:", err)
	}
	totalAnswer := ""
	toolCallID := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			toolCallID = ev.ToolCalls[0].ID
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
		}
	}

	i2, err := client.RunWithFunctionCall(appbuilder.AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		ToolOutputs: []appbuilder.ToolOutput{
			{
				ToolCallID: toolCallID,
				Output:     "北京今天35度",
			},
		},
		Stream: true,
	})

	if err != nil {
		fmt.Println("run failed: ", err)
	}

	for answer, err := i2.Next(); err == nil; answer, err = i2.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
		}
	}

	fmt.Println("----------------answer-------------------")
	fmt.Println(totalAnswer)
}
```

