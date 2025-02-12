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
	"strings"
	"testing"
)

func TestNewAppBuilderClientError(t *testing.T) {
	t.Parallel() // 并发运行
	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	// NewAppBuilderClient测试1
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	_, err = NewAppBuilderClient("", config)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
	}
	// NewAppBuilderClient测试2
	_, err = NewAppBuilderClient(appID, nil)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
	}

	// GetSdkConfig测试
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AppBuilderClient instance failed")
	}
	client.GetSdkConfig()
	// GetClient测试
	client.GetClient()

	var GatewayURL = config.GatewayURLV2

	// CreateConversation 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.CreateConversation()
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}
	// CreateConversation 测试2  Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.CreateConversation()
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected Bad Request error, got %v", err)
	}
	// CreateConversation 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.CreateConversation()
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}
	// CreateConversation 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.CreateConversation()
	if err == nil {
		t.Fatalf("expected read error, got nil")
	}

	// CreateConversation 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.CreateConversation()
	if err == nil {
		t.Fatalf("expected JSON unmarshal error, got nil")
	}
	// CreateConversation 测试 6: 缺少 id 字段
	client.client = &MissingIDHTTPClient{}
	client.CreateConversation()

	// 测试1  ServiceURLV2 错误
	config.GatewayURLV2 = "://invalid-url"
	_, err = GetAppList(GetAppListRequest{
		Limit: 10,
	}, config)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}
	// 测试2  Do 错误
	config.GatewayURLV2 = "http://192.0.2.1"
	_, err = GetAppList(GetAppListRequest{
		Limit: 10,
	}, config)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected Bad Request error, got %v", err)
	}

	// 测试3  错误的 HTTP 响应
	config.GatewayURLV2 = GatewayURL
	config.HTTPClient = &MockHTTPClient{}
	_, err = GetAppList(GetAppListRequest{
		Limit: 10,
	}, config)
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}
	// 测试 4: 模拟读取 body 时发生错误
	config.GatewayURLV2 = GatewayURL
	config.HTTPClient = &FaultyHTTPClient{}
	_, err = GetAppList(GetAppListRequest{
		Limit: 10,
	}, config)
	if err == nil {
		t.Fatalf("expected read error, got nil")
	}

	// 测试 5: json.Unmarshal错误
	config.GatewayURLV2 = GatewayURL
	config.HTTPClient = &InvalidJSONHTTPClient{}
	_, err = GetAppList(GetAppListRequest{
		Limit: 10,
	}, config)
	if err == nil {
		t.Fatalf("expected JSON unmarshal error, got nil")
	}
}

func TestClientUploadLocalFile(t *testing.T) {
	t.Parallel() // 并发运行
	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	var GatewayURL = config.GatewayURLV2
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AppBuilderClient instance failed")
	}
	// 测试 UploadLocalFile 1: 文件打开错误
	_, err = client.UploadLocalFile("validConversationID", "invalidFilePath")
	if err == nil || !strings.Contains(err.Error(), "no such file or directory") {
		t.Errorf("expected file open error, got %v", err)
	}
	// 测试 UploadLocalFile 2: t.client.Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.UploadLocalFile("5678987", "./files/test.pdf")
	if err == nil {
		t.Errorf("expected client error, got nil")
	}

	// 测试 UploadLocalFile 3: 无效的ServiceURLV2
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.UploadLocalFile("12345", "./files/test.pdf")
	if err == nil || !strings.Contains(err.Error(), "missing protocol scheme") {
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}

	// 测试 UploadLocalFile 4: 错误的 HTTP 响应
	client.client = &MockHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadLocalFile("21", "./files/test.pdf")
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}
	// 测试 UploadLocalFile 5: 模拟读取 body 时发生错误
	client.client = &FaultyHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadLocalFile("22", "./files/test.pdf")
	if err == nil {
		t.Fatalf("expected read error, got nil")
	}
	// 测试 UploadLocalFile 6: json.Unmarshal错误
	client.client = &InvalidJSONHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadLocalFile("11", "./files/test.pdf")
	if err == nil {
		t.Fatalf("expected JSON unmarshal error, got nil")
	}
	// 测试 UploadLocalFile 7: 缺少 id 字段
	client.client = &MissingIDHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadLocalFile("23", "./files/test.pdf")
	if err == nil {
		t.Fatalf("expected missing conversation_id error, got nil")
	}
}

func TestClientRun(t *testing.T) {
	t.Parallel() // 并发运行
	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	var GatewayURL = config.GatewayURLV2
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AppBuilderClient instance failed")
	}
	// 测试1 conversationID ==0
	_, err = client.Run("", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Errorf("expected conversationID mustn't be empty, got %v", err)
	}

	// 测试2   ServiceURLV2 error 无效的ServiceURLV2
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.Run("12", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}
	// 测试3   t.client.Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.Run("123", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected Bad Request error, got %v", err)
	}
	// 测试4   错误的 HTTP 响应
	client.client = &MockHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.Run("1234", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}
}

func TestClientRunWithToolCallError(t *testing.T) {
	t.Parallel() // 并发运行
	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	var GatewayURL = config.GatewayURLV2
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	client, err := NewAppBuilderClient(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AppBuilderClient instance failed")
	}
	jsonStr := `
	{
		"type": "function",
		"function": {
			"name": "get_cur_whether",
			"description": "这是一个获得指定地点天气的工具",
			"parameters": {
				"type": "object",
				"properties": {
					"location": {
						"type": "string",
						"description": "省，市名，例如：河北省"
					},
					"unit": {
						"type": "string",
						"enum": ["摄氏度", "华氏度"]
					}
				},
				"required": ["location"]
			}
		}
	}`

	var tool Tool
	err = json.Unmarshal([]byte(jsonStr), &tool)
	if err != nil {
		fmt.Println("unmarshal tool error:", err)
	}

	// 测试1 conversationID ==0
	client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: "",
		Stream:         false,
		Tools:          []Tool{tool},
	})

	// 测试4   非流式
	client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: "111111",
		Stream:         false,
		Tools:          []Tool{tool},
	})

	// 测试2   ServiceURLV2 error 无效的ServiceURLV2
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: "111111111",
		Stream:         false,
		Tools:          []Tool{tool},
	})

	// 测试3   t.client.Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: "222222",
		Stream:         false,
		Tools:          []Tool{tool},
	})

	// 测试4   错误的 HTTP 响应
	client.client = &MockHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: "33333",
		Stream:         false,
		Tools:          []Tool{tool},
	})
}

func TestNewAppBuilderClient(t *testing.T) {
	var logBuffer bytes.Buffer

	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	// 定义一个日志函数，将日志写入缓冲区
	log := func(format string, args ...any) {
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

	maxKeys := 10
	apps2, err := DescribeApps(DescribeAppsRequest{MaxKeys: &maxKeys}, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("describe apps failed: %v", err)
	}
	log("Number of apps: %d", len(apps2.Data))

	appID := "fb64d96b-f828-4385-ba1d-835298d635a9"
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
	// test follow up queries
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer += answer.Answer
		for _, ev := range answer.Events {
			if ev.ContentType == JsonContentType {
				detail := ev.Detail.(JsonDetail)
				folllowUpQueries := detail.Json.FollowUpQueries
				fmt.Println(folllowUpQueries)
				if len(folllowUpQueries[0]) == 0 {
					t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
					t.Fatal("follow up queries is empty")
				}
			}
			evJSON, _ := json.Marshal(ev)
			log(string(evJSON))
		}
	}
	log("----------------answer-------------------")
	log(totalAnswer)
	// 测试4   非流式
	client.Run(conversationID, "描述简历中的候选人情况", nil, false)

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else { // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestAppBuilderClientRunWithToolCall(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	log := func(format string, args ...any) {
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

	jsonStr := `
	{
		"type": "function",
		"function": {
			"name": "get_cur_whether",
			"description": "这是一个获得指定地点天气的工具",
			"parameters": {
				"type": "object",
				"properties": {
					"location": {
						"type": "string",
						"description": "省，市名，例如：河北省"
					},
					"unit": {
						"type": "string",
						"enum": ["摄氏度", "华氏度"]
					}
				},
				"required": ["location"]
			}
		}
	}`

	var tool Tool
	err = json.Unmarshal([]byte(jsonStr), &tool)
	if err != nil {
		fmt.Println("unmarshal tool error:", err)
	}

	i, err := client.RunWithToolCall(AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: conversationID,
		Stream:         false,
		Tools:          []Tool{tool},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	totalAnswer := ""
	toolCallID := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer += answer.Answer
		lastEvent := answer.Events[len(answer.Events)-1]
		toolCallID = lastEvent.ToolCalls[len(lastEvent.ToolCalls)-1].ID
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
	} else { // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestAppBuilderClientRunToolChoice(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	log := func(format string, args ...any) {
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
	i, err := client.Run(AppBuilderClientRunRequest{
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
	} else { // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestAppBuilderClientRunChatflow(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")

	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	appID := "4403205e-fb83-4fac-96d8-943bdb63796f"
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

	i, err := client.Run(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "查天气",
		Stream:         true,
	})

	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}

	var interruptId string
	interruptStack := make([]string, 0)
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == PublishMessageContentType {
				detail := ev.Detail.(PublishMessageDetail)
				message := detail.Message
				fmt.Println(message)
				break
			}
			if ev.ContentType == ChatflowInterruptContentType {
				deatil := ev.Detail.(ChatflowInterruptDetail)
				interruptId = deatil.InterruptEventID
				interruptStack = append(interruptStack, interruptId)
				break
			}
		}
	}
	if len(interruptId) == 0 {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("interrupt id is empty")
	}

	interruptId = ""
	i2, err := client.Run(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "我先查个航班动态",
		Stream:         true,
		Action:         NewResumeAction(interruptStack[len(interruptStack)-1]),
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	interruptStack = interruptStack[:len(interruptStack)-1]
	for answer, err := i2.Next(); err == nil; answer, err = i2.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == PublishMessageContentType {
				detail := ev.Detail.(PublishMessageDetail)
				message := detail.Message
				fmt.Println(message)
				break
			}
			if ev.ContentType == ChatflowInterruptContentType {
				deatil := ev.Detail.(ChatflowInterruptDetail)
				interruptId = deatil.InterruptEventID
				interruptStack = append(interruptStack, interruptId)
				break
			}
		}
	}
	if len(interruptId) == 0 {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("interrupt id is empty")
	}

	interruptId = ""
	i3, err := client.Run(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "CA1234",
		Stream:         true,
		Action:         NewResumeAction(interruptStack[len(interruptStack)-1]),
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	interruptStack = interruptStack[:len(interruptStack)-1]
	for answer, err := i3.Next(); err == nil; answer, err = i3.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == TextContentType {
				detail := ev.Detail.(TextDetail)
				text := detail.Text
				fmt.Println(text)
				break
			}
			if ev.ContentType == ChatflowInterruptContentType {
				deatil := ev.Detail.(ChatflowInterruptDetail)
				interruptId = deatil.InterruptEventID
				interruptStack = append(interruptStack, interruptId)
				break
			}
		}
	}
	if len(interruptId) == 0 {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("interrupt id is empty")
	}

	i4, err := client.Run(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "北京的",
		Stream:         true,
		Action:         NewResumeAction(interruptStack[len(interruptStack)-1]),
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	for answer, err := i4.Next(); err == nil; answer, err = i4.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == TextContentType {
				detail := ev.Detail.(TextDetail)
				text := detail.Text
				fmt.Println(text)
				break
			}
		}
	}

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else { // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestAppbuilderClientFeedback(t *testing.T) {
	var logBuffer bytes.Buffer

	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "fb64d96b-f828-4385-ba1d-835298d635a9"
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

	i, err := client.Run(conversationID, "描述简历中的候选人情况", nil, false)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}

	var messageID string
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		if answer.MessageID != "" {
			messageID = answer.MessageID
			break
		}
	}

	_, err = client.Feedback(AppBuilderClientFeedbackRequest{
		ConversationID: conversationID,
		MessageID:      messageID,
		Type:           "downvote",
		Flag:           []string{"没有帮助"},
		Reason:         "测试",
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upvote failed:%v", err)
	}

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else { // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}
