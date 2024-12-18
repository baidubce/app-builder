# ToolChoice

#### Run方法带ToolChoice使用示例：

* 注意：当前功能为试运行阶段，可能存在如下问题，如使用过程遇到其他问题，欢迎提issue或微信群讨论。
  * 需开启"组件/知识库结论可直接作为回复"
  * 组件名称不是界面上的原始名字，而是个人空间组件列表中的英文名
  * 自定义组件的参数不能使用系统参数，可以使用用户添加的参数
  * 部分官方组件使用的参数与界面上的参数不一致

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."

app_id = "..."  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()

# 注意使用创建应用中用到的组件。名称、参数均以实际使用的组件为准。
answer = app_builder_client.run(
    conversation_id,
    "北京今天的天气",
    stream=False,
    end_user_id="user_id_toolchoice",
    tool_choice={
        "type": "function",
        "function": {"name": "WeatherQuery", "input": {"city": "北京"}},
    },
)
```

#### Run方法带Toolchoice使用示例--Java

* 注意：当前功能为试运行阶段，可能存在如下问题，如使用过程遇到其他问题，欢迎提issue或微信群讨论。

  * 需开启"组件/知识库结论可直接作为回复"

  * 组件名称不是界面上的原始名字，而是个人空间组件列表中的英文名

  * 自定义组件的参数不能使用系统参数，可以使用用户添加的参数

  * 部分官方组件使用的参数与界面上的参数不一致

```java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String appId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();

        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "你能干什么", false);
        request.setEndUserId("java_toolchoice_demo");
      
        // 注意使用创建应用中用到的组件。名称、参数均以实际使用的组件为准。
        Map<String, Object> input = new HashMap<>();
        input.put("city", "北京");
        AppBuilderClientRunRequest.ToolChoice.Function func = new AppBuilderClientRunRequest.ToolChoice.Function(
                "WeatherQuery", input);
        AppBuilderClientRunRequest.ToolChoice choice = new AppBuilderClientRunRequest.ToolChoice("function", func);
        request.setToolChoice(choice);

        AppBuilderClientIterator itor = builder.run(request);
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }
}

```


#### ToolChoice示例代码--Go

* 注意：当前功能为试运行阶段，可能存在如下问题，如使用过程遇到其他问题，欢迎提issue或微信群讨论。

  * 需开启"组件/知识库结论可直接作为回复"

  * 组件名称不是界面上的原始名字，而是个人空间组件列表中的英文名
  
  * 自定义组件的参数不能使用系统参数，可以使用用户添加的参数

  * 部分官方组件使用的参数与界面上的参数不一致


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

    // 注意使用创建应用中用到的组件。名称、参数均以实际使用的组件为准。
	input := make(map[string]any)
	input["city"] = "北京"
	end_user_id := "go_toolchoice_demo"
	i, err := client.Run(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "",
		EndUserID:      &end_user_id,
		Stream:         false,
		ToolChoice: &ToolChoice{
			Type: "function",
			Function: ToolChoiceFunction{
				Name:  "WeatherQuery",
				Input: input,
			},
		},
	})
  
	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}

    for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
		}
	}
}
```