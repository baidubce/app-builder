// Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package appbuilder

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"testing"
)

func TestNewAppBuilderClient(t *testing.T) {
	var logBuffer bytes.Buffer

	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	// 定义一个日志函数，将日志写入缓冲区
	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	apps, err := GetAppList(GetAppListRequest{
		Limit: 10,
	}, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("get apps failed: %v", err)
	}
	log("Number of apps: %d", len(apps))

	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AppBuilderClient instance failed")
	}

	conversationID, err := client.CreateConversation()
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create conversation failed: %v", err)
	}
	_, err = client.UploadLocalFile(conversationID, "./files/test.pdf")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upload local file failed: %v", err)
	}
	i, err := client.Run(conversationID, "描述简历中的候选人情况", nil, true)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	totalAnswer := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer += answer.Answer
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			log(string(evJSON))
		}
	}
	log("----------------answer-------------------")
	log(totalAnswer)

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestAppBuilderClientRunWithToolCall(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AgentBuidler instance failed")
	}

	conversationID, err := client.CreateConversation()
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create conversation failed: %v", err)
	}

	parameters := make(map[string]any)

	location := make(map[string]any)
	location["type"] = "string"
	location["description"] = "省，市名，例如：河北省"

	unit := make(map[string]any)
	unit["type"] = "string"
	unit["enum"] = []string{"摄氏度", "华氏度"}

	properties := make(map[string]any)
	properties["location"] = location
	properties["unit"] = unit

	parameters["type"] = "object"
	parameters["properties"] = properties
	parameters["required"] = []string{"location"}

	i, err := client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: conversationID,
		Stream:         false,
		Tools: []Tool{
			{
				Type: "function",
				Function: Function{
					Name:        "get_cur_whether",
					Description: "这是一个获得指定地点天气的工具",
					Parameters:  parameters,
				},
			},
		},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	totalAnswer := ""
	toolCallID := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer += answer.Answer
		for _, ev := range answer.Events {
			toolCallID = ev.ToolCalls[0].ID
			evJSON, _ := json.Marshal(ev)
			log(string(evJSON))
		}
	}

	i2, err := client.RunWithToolCall(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		ToolOutputs: []ToolOutput{
			{
				ToolCallID: toolCallID,
				Output:     "北京今天35",
			},
		},
	})

	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}

	for answer, err := i2.Next(); err == nil; answer, err = i2.Next() {
		totalAnswer += answer.Answer
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			log(string(evJSON))
		}
	}

	log("----------------answer-------------------")
	log(totalAnswer)

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		fmt.Printf("%s========== FAIL:  %s ==========%s\n", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestAppBuilderClientRunToolChoice(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AgentBuidler instance failed")
	}

	conversationID, err := client.CreateConversation()
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create conversation failed: %v", err)
	}

	input := make(map[string]any)
	input["city"] = "北京"
	end_user_id := "go_user_id_0"
	i, err := client.RunWithToolCall(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "你能干什么",
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
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}

	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			log(string(evJSON))
		}
	}

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}