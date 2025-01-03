# ComponentClient

## 简介

ComponentClient组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)平台上创建的自定义工作流组件。

### 功能介绍

具体包括运行等。

### 特色优势

与云端工作流组件能力打通，实现低代码会话

### 应用场景

快速、高效集成云端工作流组件能力


### `ComponentClient().run() -> Message`

#### 方法参数

| 参数名称             | 参数类型 | 是否必须 | 描述                                                         | 示例值            |
| -------------------- | -------- | -------- | ------------------------------------------------------------ | ----------------- |
| component_id         | String   | 是       | 组件ID。可以在个人空间-组件下查看。                          |                   |
| sys_origin_query     | String   | 是       | query问题内容                                                | "今天天气怎么样?" |
| version              | String   | 否       | 组件版本                                                     |                   |
| stream               | Bool     | 否       | 为true时则流式返回，为false时则一次性返回所有内容, 默认为false | False             |
| action               | String   | 否       | 调用方式。<br/>默认值是tool_eval。                           |                   |
| sys_file_urls        | Dict     | 否       | 文件路径。对应画布中开始节点的系统参数fileUrls，格式为{"文件名": "文件路径"}，例如{"xxx.pdf": "http:///"}。 |                   |
| sys_conversatiaon_id | String   | 否       | 对话id。对应画布中开始节点的系统参数conversation_id，可通过新建会话接口创建。 |                   |
| sys_chat_history     | Dict     | 否       | 组件使用的累计对话历史。对应画布中开始节点的系统参数chatHistory。{"role": "", "content": ""} |                   |
| sys_end_user_id      | String   | 否       | 终端用户id。对应画布中开始节点的系统参数end_user_id。        |                   |
| input_variable_name  | Object   | 否       | 用户自定义参数                                               |                   |

#### Run方法非流式返回值

Run非流式方法返回一个`Message`对象，`Message`通过`RunResponse`封装，该对象包含以下属性：

| 参数名称        | 参数类型      | 是否必填 | 示例值                                                       |
| --------------- | ------------- | -------- | ------------------------------------------------------------ |
| conversation_id | string        | 是       | 会话标识UUID。                                               |
| message_id      | string        | 是       | 一问或一答的标识UUID。                                       |
| trace_id        | string        | 是       | 调用标识UUID。                                               |
| user_id         | string        | 是       | 开发者UUID（计费依赖）。                                     |
| end_user_id     | string        | 否       | 终端用户ID。                                                 |
| is_completion   | bool          | 是       | 标识当前端到端的流式调用是否结束。                           |
| role            | string        | 是       | 当前消息来源，默认tool 。                                    |
| content         | list[Content] | 否       | 当前组件返回内容的主要payload，List[Content]，每个 Content 包括了当前 event 的一个元素，具体见下文Content对象定义。 |

`Content`类型定义如下：

| 参数名称      | 参数类型    | 是否必填 | 示例值                                                       |
| ------------- | ----------- | -------- | ------------------------------------------------------------ |
| type          | string      | 是       | 代表event 类型。该字段的取值决定了下面`text`字段的内容结构。  枚举值： text、json、code、files、urls、oral_text、references、image、chart、audio、function_call。 |
| name          | string      | 是       | 介绍当前yield内容的step name。                               |
| text          | dict object | 是       | 代表当前 event 元素的内容，每一种 event 对应的 text 结构固定。 |
| visible_scope | string      | 是       | 可见范围。  枚举值： all ：全部，包括大模型和用户。 llm：大模型。 user：用户。 默认为all。 |
| usage         | dict        | 否       | 大模型的token用量，具体见下文Usage对象定义。                 |
| metrics       | dict        | 是       | 耗时信息，具体见下文Metrics对象定义。                        |
| event         | dict        | 是       | 标识返回内容的结构、顺序、状态，具体见下文Event对象定义。    |

**Usage对象**

| **字段**          | **类型**   | **必填** | **说明**                                                     |
| ----------------- | ---------- | -------- | ------------------------------------------------------------ |
| prompt_tokens     | int        | 是       | 输入token消耗                                                |
| completion_tokens | int        | 是       | 输出token消耗                                                |
| total_tokens      | int        | 是       | 总token消耗                                                  |
| nodes             | list[node] | 否       | 工作流节点大模型token消耗信息，列表元素具体见下文Node对象定义。 |

**Node对象**

| **字段**     | **类型**          | **必填** | **说明**                                      |
| ------------ | ----------------- | -------- | --------------------------------------------- |
| node_id      | string            | 是       | 节点id                                        |
| models_usage | list[model_usage] | 是       | 模型消耗列表，元素见下文model_usage对象定义。 |

**model_usage对象**

| **字段**          | **类型** | **必填** | **说明**      |
| ----------------- | -------- | -------- | ------------- |
| model_name        | string   | 是       | 模型名称      |
| prompt_tokens     | int      | 是       | 输入token消耗 |
| completion_tokens | int      | 是       | 输出token消耗 |
| total_tokens      | int      | 是       | 总token消耗   |

**Metrics对象**

| **字段**   | **类型** | **必填** | **说明**                                            |
| ---------- | -------- | -------- | --------------------------------------------------- |
| begin_time | string   | 是       | 请求开始时间，示例：”2000-01-01T10:00:00.560430“。  |
| duration   | float    | 是       | 从请求到当前event总耗时，保留3位有效数字，单位秒s。 |

**Event对象**

| **字段**      | **类型** | **必填** | **说明**                                                     |
| ------------- | -------- | -------- | ------------------------------------------------------------ |
| id            | string   | 是       | 节点id。                                                     |
| status        | string   | 是       | 事件执行状态。  枚举值： preparing：运行中。 running：运行中。 error：错误。 done：执行完成。 |
| name          | string   | 是       | 事件名。  一级深度有： component，组件api。 functioncall，自主规划agent。 chatflow，工作流agent。 二级深度是组件ID。 三级深度是组件content_type。  示例： /component/eaaccc60e222418abc0f4d3d372018af/node/ 433b4cf184064daf88e8383adc83e35f |
| created_time  | string   | 是       | 当前event发送时间。                                          |
| error_code    | string   | 否       | 错误码。                                                     |
| error_message | string   | 否       | 错误细节。                                                   |

#### Run方法流式返回值

| 参数名称 | 参数类型         | 描述                                  | 示例值 |
| -------- | ---------------- | ------------------------------------- | ------ |
| content  | Python Generator | 可迭代，每次迭代返回`RunResponse`类型 | 无     |

#### 非流式调用示例

```python
import os
import appbuilder


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = (
    "..."
)

# 组件ID，可在个人空间-组件下查看
component_id = "..."
client = appbuilder.ComponentClient()
message = client.run(component_id=component_id, version="latest",
                 stream=False, sys_origin_query="北京景点推荐")
print(message.content.content[0].text)
```

#### 流式调用示例

```python
import os
import appbuilder


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = (
    "..."
)

# 组件ID，可在个人空间-组件下查看
component_id = "..."
client = appbuilder.ComponentClient()
message = client.run(component_id=component_id, version="latest",
                     stream=True, sys_origin_query="北京景点推荐")
for content in message.content:
    if len(content.content)>0:
        print(content.content[0].text)

```

## Java基本用法

### ```new ComponentClient()```


#### 方法返回值

```ComponentClient```实例化对象

### ```ComponentClient().run()```

#### run方法入参

| 参数名称               | 参数类型 | 是否必须 | 描述                                                         | 示例值 |
| ---------------------- | -------- | -------- | ------------------------------------------------------------ | ------ |
| componentId            | String   | 是       | 组件ID。可以在个人空间-组件下查看。                          |        |
| version                | String   | 否       | 组件版本                                                     |        |
| action                 | String   | 否       | 调用方式。<br/>默认值是tool_eval。                           |        |
| stream                 | Bool     | 是       | 为true时则流式返回，为false时则一次性返回所有内容, 默认为false | false  |
| parameters             | Map      | 是       | 调用传参                                                     |        |
| +_sys_origin_query     | string   | 是       | 用户query，对应画布中开始节点的系统参数rawQuery。            |        |
| +_sys_file_urls        | Dict     | 否       | 文件路径。对应画布中开始节点的系统参数fileUrls，格式为{"文件名": "文件路径"}，例如{"xxx.pdf": "http:///"}。 |        |
| +_sys_conversatiaon_id | String   | 否       | 对话id。对应画布中开始节点的系统参数conversation_id，可通过新建会话接口创建。 |        |
| +_sys_chat_history     | Dict     | 否       | 组件使用的累计对话历史。对应画布中开始节点的系统参数chatHistory。{"role": "", "content": ""} |        |
| +_sys_end_user_id      | String   | 否       | 终端用户id。对应画布中开始节点的系统参数end_user_id。        |        |
| + input_variable_name  | object   | 否       | 用户自定义添加的参数，对应画布中开始节点用户新增的参数。注意，用户自定义参数和系统参数为一级，同在**parameters中。**例如：<br /><br />"parameters":<br /> {         <br />"_sys_origin_query": "今天有什么新闻",        <br /> "custom_count": 4    <br /> }<br /> |        |

#### run方法出参
| 参数名称                | 参数类型                | 描述                                                         | 示例值 |
| ----------------------- | ----------------------- | ------------------------------------------------------------ | ------ |
| ComponentClientIterator | ComponentClientIterator | 回答迭代器，流式/非流式均统一返回该类型,每次迭代返回ComponentClientIterator类型 |        |

#### 迭代ComponentClientIterator

| **字段**       | **类型**          | **必填** | **说明**                                                     |
| -------------- | ----------------- | -------- | ------------------------------------------------------------ |
| conversationID | string            | 是       | 会话标识UUID。                                               |
| messageID      | string            | 是       | 一问或一答的标识UUID。                                       |
| traceID        | string            | 是       | 调用标识UUID。                                               |
| userID         | string            | 是       | 开发者UUID（计费依赖）。                                     |
| endUserId      | string            | 否       | 终端用户ID。                                                 |
| isCompletion   | bool              | 是       | 标识当前端到端的流式调用是否结束。                           |
| role           | string            | 是       | 当前消息来源，默认tool 。                                    |
| **content**    | **list[Content]** | **否**   | **当前组件返回内容的主要payload，List[Content]，每个 Content 包括了当前 event 的一个元素，具体见下文Content对象定义。** |

**Content对象**

| **字段**     | **类型**    | **必填** | **说明**                                                     |
| ------------ | ----------- | -------- | ------------------------------------------------------------ |
| type         | string      | 是       | 代表event 类型，该字段的取值决定了下面`text`字段的内容结构。枚举值： text、json、code、files、urls、oral_text、references、image、chart、audio、function_call |
| name         | string      | 是       | 介绍当前yield内容的step name                                 |
| text         | dict object | 是       | 代表当前 event 元素的内容，每一种 event 对应的 text 结构固定。 |
| visibleScope | string      | 是       | 可见范围。枚举值：all ：全部，包括大模型和用户llm：大模型user：用户默认为all |
| **usage**    | **dict**    | **否**   | **大模型的token用量，具体见下文Usage对象定义。**             |
| **metrics**  | **dict**    | **是**   | **耗时信息，具体见下文Metrics对象定义。**                    |
| **event**    | **dict**    | **是**   | **标识返回内容的结构、顺序、状态，具体见下文Event对象定义。** |

**Usage对象**

| **字段**          | **类型**       | **必填** | **说明**                                                     |
| ----------------- | -------------- | -------- | ------------------------------------------------------------ |
| prompt_tokens     | int            | 是       | 输入token消耗                                                |
| completion_tokens | int            | 是       | 输出token消耗                                                |
| total_tokens      | int            | 是       | 总token消耗                                                  |
| **nodes**         | **list[node]** | **否**   | **工作流节点大模型token消耗信息，列表元素****具体见下文Node对象定义。** |

**Node对象**

| **字段**         | **类型**              | **必填** | **说明**                                          |
| ---------------- | --------------------- | -------- | ------------------------------------------------- |
| node_id          | string                | 是       | 节点id                                            |
| **models_usage** | **list[model_usage]** | **是**   | **模型消耗列表，元素见下文model_usage对象定义。** |

**model_usage对象**

| **字段**          | **类型** | **必填** | **说明**      |
| ----------------- | -------- | -------- | ------------- |
| model_name        | string   | 是       | 模型名称      |
| prompt_tokens     | int      | 是       | 输入token消耗 |
| completion_tokens | int      | 是       | 输出token消耗 |
| total_tokens      | int      | 是       | 总token消耗   |

**Metrics对象**

| **字段**   | **类型** | **必填** | **说明**                                            |
| ---------- | -------- | -------- | --------------------------------------------------- |
| begin_time | string   | 是       | 请求开始时间，示例：”2000-01-01T10:00:00.560430“。  |
| duration   | float    | 是       | 从请求到当前event总耗时，保留3位有效数字，单位秒s。 |

**Event对象**

| **字段**     | **类型** | **必填** | **说明**                                                     |
| ------------ | -------- | -------- | ------------------------------------------------------------ |
| id           | string   | 是       | 节点id                                                       |
| status       | string   | 是       | 事件执行状态。枚举值：preparing：运行中running：运行中error：错误done：执行完成 |
| name         | string   | 是       | 事件名。一级深度有：component，组件apifunctioncall，自主规划agentchatflow，工作流agent二级深度是组件ID三级深度是组件content_type﻿示例：/component/eaaccc60e222418abc0f4d3d372018af/node/433b4cf184064daf88e8383adc83e35f |
| createdTime  | string   | 是       | 当前event发送时间。                                          |
| errorCode    | string   | 否       | 错误码。                                                     |
| errorMessage | string   | 否       | 错误细节。                                                   |

#### 示例代码

```Java
package com.baidubce.appbuilder.demo;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.componentclient.ComponentClient;
import com.baidubce.appbuilder.model.componentclient.ComponentClientIterator;
import com.baidubce.appbuilder.model.componentclient.ComponentClientRunRequest;
import com.baidubce.appbuilder.model.componentclient.ComponentClientRunResponse;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class ComponentClientDemo {
    public static void main(String[] args) {
        // 组件ID，可在个人空间-组件下查看
        String componentId = "...";

        try {
            ComponentClient client = new ComponentClient();
            Map<String, Object> parameters = new HashMap<>();
            parameters.put(ComponentClientRunRequest.SysOriginQuery, "北京景点推荐");

            // Run without streaming
            ComponentClientIterator iter = client.run(componentId, "latest", "", false, parameters);
            while (iter.hasNext()) {
                ComponentClientRunResponse.ComponentRunResponseData response = iter.next();
                if(response.getContent().length > 0) {
                    Map<String, Object> textMap = (Map<String, Object>) response.getContent()[0].getText();
                    System.out.println("Without streaming: " + textMap.toString());
                }
            }

            // Run with streaming
            iter = client.run(componentId, "latest", "", true, parameters);
            Map<String, Object> textMap = null;
            while (iter.hasNext()) {
                ComponentClientRunResponse.ComponentRunResponseData response = iter.next();
                if (response.getContent().length > 0) {
                    textMap = (Map<String, Object>) response.getContent()[0].getText();
                }
            }
            if (textMap != null) {
                System.out.println("With streaming: " + textMap.toString());
            }

        } catch (IOException | AppBuilderServerException e) {
            e.printStackTrace();
        }
    }
}
```



## Go基本用法

### ```NewComponentClient()```

#### 方法参数

| 参数名称 | 参数类型  | 描述        | 示例值 |
| -------- | --------- | ----------- | ------ |
| config   | SDKConfig | SDK配置信息 |        |


### `Run()`
#### Run方法入参

#### 

| 参数名称               | 参数类型 | 是否必须 | 描述                                                         | 示例值 |
| ---------------------- | -------- | -------- | ------------------------------------------------------------ | ------ |
| componentId            | String   | 是       | 组件ID。可以在个人空间-组件下查看。                          |        |
| version                | String   | 否       | 组件版本                                                     |        |
| action                 | String   | 否       | 调用方式。<br/>默认值是tool_eval。                           |        |
| stream                 | Bool     | 是       | 为true时则流式返回，为false时则一次性返回所有内容, 默认为false | false  |
| parameters             | Map      | 是       | 调用传参                                                     |        |
| +_sys_origin_query     | string   | 是       | 用户query，对应画布中开始节点的系统参数rawQuery。            |        |
| +_sys_file_urls        | Dict     | 否       | 文件路径。对应画布中开始节点的系统参数fileUrls，格式为{"文件名": "文件路径"}，例如{"xxx.pdf": "http:///"}。 |        |
| +_sys_conversatiaon_id | String   | 否       | 对话id。对应画布中开始节点的系统参数conversation_id，可通过新建会话接口创建。 |        |
| +_sys_chat_history     | Dict     | 否       | 组件使用的累计对话历史。对应画布中开始节点的系统参数chatHistory。{"role": "", "content": ""} |        |
| +_sys_end_user_id      | String   | 否       | 终端用户id。对应画布中开始节点的系统参数end_user_id。        |        |
| + input_variable_name  | object   | 否       | 用户自定义添加的参数，对应画布中开始节点用户新增的参数。注意，用户自定义参数和系统参数为一级，同在**parameters中。**例如：<br /><br />"parameters":<br /> {         <br />"_sys_origin_query": "今天有什么新闻",        <br /> "custom_count": 4    <br /> }<br /> |        |

#### Run方法出参

| 参数名称                | 参数类型                | 描述                                    | 示例值 |
| ----------------------- | ----------------------- | --------------------------------------- | ------ |
| ComponentClientIterator | ComponentClientIterator | 回答迭代器，流式/非流式均统一返回该类型 |        |
| error                   | error                   | 存在错误时error不为nil，反之            |        |

#### 迭代ComponentClientIterator

| **字段**       | **类型**          | **必填** | **说明**                                                     |
| -------------- | ----------------- | -------- | ------------------------------------------------------------ |
| ConversationID | string            | 是       | 会话标识UUID。                                               |
| MessageID      | string            | 是       | 一问或一答的标识UUID。                                       |
| TraceID        | string            | 是       | 调用标识UUID。                                               |
| UserID         | string            | 是       | 开发者UUID（计费依赖）。                                     |
| EndUserID      | string            | 否       | 终端用户ID。                                                 |
| IsCompletion   | bool              | 是       | 标识当前端到端的流式调用是否结束。                           |
| Role           | string            | 是       | 当前消息来源，默认tool 。                                    |
| **Content**    | **list[Content]** | **否**   | **当前组件返回内容的主要payload，List[Content]，每个 Content 包括了当前 event 的一个元素，具体见下文Content对象定义。** |

**Content对象**

| **字段**     | **类型**    | **必填** | **说明**                                                     |
| ------------ | ----------- | -------- | ------------------------------------------------------------ |
| Type         | string      | 是       | 代表event 类型，该字段的取值决定了下面`text`字段的内容结构。枚举值： text、json、code、files、urls、oral_text、references、image、chart、audio、function_call |
| Name         | string      | 是       | 介绍当前yield内容的step name                                 |
| Text         | dict object | 是       | 代表当前 event 元素的内容，每一种 event 对应的 text 结构固定。 |
| VisibleScope | string      | 是       | 可见范围。枚举值：all ：全部，包括大模型和用户llm：大模型user：用户默认为all |
| **Usage**    | **dict**    | **否**   | **大模型的token用量，具体见下文Usage对象定义。**             |
| **Metrics**  | **dict**    | **是**   | **耗时信息，具体见下文Metrics对象定义。**                    |
| **Event**    | **dict**    | **是**   | **标识返回内容的结构、顺序、状态，具体见下文Event对象定义。** |

**Usage对象**

| **字段**          | **类型**       | **必填** | **说明**                                                     |
| ----------------- | -------------- | -------- | ------------------------------------------------------------ |
| prompt_tokens     | int            | 是       | 输入token消耗                                                |
| completion_tokens | int            | 是       | 输出token消耗                                                |
| total_tokens      | int            | 是       | 总token消耗                                                  |
| **nodes**         | **list[node]** | **否**   | **工作流节点大模型token消耗信息，列表元素****具体见下文Node对象定义。** |

**Node对象**

| **字段**         | **类型**              | **必填** | **说明**                                          |
| ---------------- | --------------------- | -------- | ------------------------------------------------- |
| node_id          | string                | 是       | 节点id                                            |
| **models_usage** | **list[model_usage]** | **是**   | **模型消耗列表，元素见下文model_usage对象定义。** |

**model_usage对象**

| **字段**          | **类型** | **必填** | **说明**      |
| ----------------- | -------- | -------- | ------------- |
| model_name        | string   | 是       | 模型名称      |
| prompt_tokens     | int      | 是       | 输入token消耗 |
| completion_tokens | int      | 是       | 输出token消耗 |
| total_tokens      | int      | 是       | 总token消耗   |

**Metrics对象**

| **字段**   | **类型** | **必填** | **说明**                                            |
| ---------- | -------- | -------- | --------------------------------------------------- |
| begin_time | string   | 是       | 请求开始时间，示例：”2000-01-01T10:00:00.560430“。  |
| duration   | float    | 是       | 从请求到当前event总耗时，保留3位有效数字，单位秒s。 |

**Event对象**

| **字段**     | **类型** | **必填** | **说明**                                                     |
| ------------ | -------- | -------- | ------------------------------------------------------------ |
| ID           | string   | 是       | 节点id                                                       |
| Status       | string   | 是       | 事件执行状态。枚举值：preparing：运行中running：运行中error：错误done：执行完成 |
| Name         | string   | 是       | 事件名。一级深度有：component，组件apifunctioncall，自主规划agentchatflow，工作流agent二级深度是组件ID三级深度是组件content_type﻿示例：/component/eaaccc60e222418abc0f4d3d372018af/node/433b4cf184064daf88e8383adc83e35f |
| CreatedTime  | string   | 是       | 当前event发送时间。                                          |
| ErrorCode    | string   | 否       | 错误码。                                                     |
| ErrorMessage | string   | 否       | 错误细节。                                                   |


#### Run示例代码


```Go
// 安装说明：
// 支持Go 1.18以上版本
// go get github.com/baidubce/app-builder/go/appbuilder

package main

import (
	"fmt"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")
  // 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
	config, err := appbuilder.NewSDKConfig("", "...")
	if err != nil {
		fmt.Println("new http client config failed: ", err)
	}

  // 组件ID，可在个人空间-组件下查看
	componentID := "..."
	client, err := appbuilder.NewComponentClient(config)
	if err != nil {
		fmt.Println("new ComponentClient instance failed")
	}

	parameters := map[string]any{
		appbuilder.SysOriginQuery: "北京景点推荐",
	}
	ans, err := client.Run(componentID, "latest", "", false, parameters)
	if err != nil {
		fmt.Println("run component failed: " + err.Error())
	}

	// run non stream
	for answer, err := ans.Next(); err == nil; answer, err = ans.Next() {
		data := answer.Content[0].Text
		if data == nil {
			fmt.Println("run component failed: data is nil")
			return
		}
		fmt.Println("run component result: ")
		fmt.Println(data)
	}

	// run stream
	streamAns, err := client.Run(componentID, "latest", "", true, parameters)
	if err != nil {
		fmt.Println("run component failed: " + err.Error())
	}
	var answerText any
	for answer, err := streamAns.Next(); err == nil; answer, err = streamAns.Next() {
		if len(answer.Content) == 0 {
			continue
		}
		answerText = answer.Content[0].Text
	}
	if answerText == nil {
		fmt.Println("run component failed: answer is nil")
		return
	}
	fmt.Println("run component result: ")
	fmt.Println(answerText)
}

```
