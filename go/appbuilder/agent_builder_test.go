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
	"net/http"
    "io"
    "strings"
    "testing"
)

// 模拟返回 400 错误的 HTTP 响应
type MockHTTPClient struct{}

func (m *MockHTTPClient) Do(req *http.Request) (*http.Response, error) {
    return &http.Response{
        StatusCode: 400,  // 非 2xx 状态码
        Body:       io.NopCloser(strings.NewReader(`{"error": "Bad Request"}`)),
    }, nil
}

// FaultyHTTPClient 模拟响应读取时发生错误
type FaultyHTTPClient struct{}

func (f *FaultyHTTPClient) Do(req *http.Request) (*http.Response, error) {
    return &http.Response{
        StatusCode: 200,  // 返回成功的状态码
        Body:       &FaultyBody{},  // 使用 FaultyBody，模拟读取时出错
    }, nil
}

// FaultyBody 模拟响应体读取错误
type FaultyBody struct{}

func (f *FaultyBody) Read(p []byte) (n int, err error) {
    return 0, fmt.Errorf("simulated read error")  // 模拟读取时发生错误
}

func (f *FaultyBody) Close() error {
    return nil
}

// 模拟无效 JSON 响应
type InvalidJSONHTTPClient struct{}

func (m *InvalidJSONHTTPClient) Do(req *http.Request) (*http.Response, error) {
    return &http.Response{
        StatusCode: 200,
        Body:       io.NopCloser(strings.NewReader(`{invalid_json}`)),
    }, nil
}

// 模拟缺少 id 的 JSON 响应
type MissingIDHTTPClient struct{}

func (m *MissingIDHTTPClient) Do(req *http.Request) (*http.Response, error) {
    return &http.Response{
        StatusCode: 200,  // 成功的状态码，但缺少 id 字段
        Body:       io.NopCloser(strings.NewReader(`{"message": "Upload successful", "other_field": "value"}`)), // 缺少 id 字段
    }, nil
}
func TestNewAgentBuilderError(t *testing.T) {
	t.Parallel() // 并发运行
	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")

	// NewAgentBuilder测试 1: appID 为空，预期返回错误
	_, err := NewAgentBuilder("", &SDKConfig{})
	if err == nil || err.Error() != "appID is empty" {
		t.Errorf("expected error for empty appID, got %v", err)
	}

	// NewAgentBuilder测试 2: config 为 nil，预期返回错误
	_, err = NewAgentBuilder("validAppID", nil)
	if err == nil || err.Error() != "config is nil" {
		t.Errorf("expected error for nil config, got %v", err)
	}

	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"

	// CreateConversation测试 1: ServiceURLV2 错误
	agentBuilder, err := NewAgentBuilder(appID, config)
	if err != nil {
		t.Fatalf("new AgentBuilder instance failed")
	}
	agentBuilder.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = agentBuilder.CreateConversation()
	if err == nil {
		t.Errorf("expected ServiceURLV2 error, got nil")
	}

	// CreateConversation测试 2: HTTP client do error
	agentBuilder.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = agentBuilder.CreateConversation()
	if err == nil {
		t.Errorf("expected client error, got nil")
	}

	// CreateConversation测试 3: checkHTTPResponse 400 错误
	agentBuilder.client = &MockHTTPClient{}
	_, err = agentBuilder.CreateConversation()
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}

	// CreateConversation测试 4: 模拟读取 body 时发生错误
	agentBuilder.client = &FaultyHTTPClient{}
	_, err = agentBuilder.CreateConversation()
	if err == nil {
		t.Fatalf("expected read error, got nil")
	}

	// CreateConversation测试 5: json.Unmarshal错误
	agentBuilder.client = &InvalidJSONHTTPClient{}
	_, err = agentBuilder.CreateConversation()
	if err == nil {
		t.Fatalf("expected JSON unmarshal error, got nil")
	}

	// CreateConversation测试 6: 缺少 conversation_id
	agentBuilder.client = &MissingIDHTTPClient{}
	_, err = agentBuilder.CreateConversation()
	if err == nil {
		t.Fatalf("expected missing conversation_id error, got nil")
	}

}
func TestNewAgentBuilderUploadLocalFileError1(t *testing.T) {
	t.Parallel() // 并发运行
	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	//正常的agentBuilder
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	agentBuilder, _ := NewAgentBuilder(appID, config)

	// 测试 UploadLocalFile 1: 文件打开错误
	_, err = agentBuilder.UploadLocalFile("validConversationID", "invalidFilePath")
	if err == nil || !strings.Contains(err.Error(), "no such file or directory") {
		t.Errorf("expected file open error, got %v", err)
	}

	// 测试 UploadLocalFile 2: 文件复制错误


	// 测试 UploadLocalFile 4: t.client.Do 错误
	agentBuilder.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = agentBuilder.UploadLocalFile("5665", "./files/test.pdf")
	if err == nil {
		t.Errorf("expected client error, got nil")
	}

	// 测试 UploadLocalFile 3: 无效的ServiceURLV2
	agentBuilder.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = agentBuilder.UploadLocalFile("6776", "./files/test.pdf")
	if err == nil || !strings.Contains(err.Error(), "missing protocol scheme") {
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}


}
func TestNewAgentBuilderUploadLocalFileError2(t *testing.T) {
	t.Parallel() // 并发运行
	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	//正常的agentBuilder
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	agentBuilder, _ := NewAgentBuilder(appID, config)

	// 测试 UploadLocalFile 5: checkHTTPResponse 错误
	agentBuilder.client = &MockHTTPClient{}
	_, err = agentBuilder.UploadLocalFile("123321", "./files/test.pdf")
	if err == nil || !strings.Contains(err.Error(), "Bad Request") {
		t.Errorf("expected Bad Request error, got %v", err)
	}
	// 测试 UploadLocalFile 6: io.ReadAll 错误
	agentBuilder.client = &FaultyHTTPClient{}
	_, err = agentBuilder.UploadLocalFile("2332", "./files/test.pdf")
	if err == nil || !strings.Contains(err.Error(), "simulated read error") {
		t.Errorf("expected read error, got %v", err)
	}

	// 测试 UploadLocalFile 7: json.Unmarshal 错误
	agentBuilder.client = &InvalidJSONHTTPClient{}
	_, err = agentBuilder.UploadLocalFile("3443", "./files/test.pdf")
	if err == nil || !strings.Contains(err.Error(), "invalid character") {
		t.Errorf("expected JSON unmarshal error, got %v", err)
	}

	// 测试 UploadLocalFile 8: 缺少 id 字段
	agentBuilder.client = &MissingIDHTTPClient{}
	_, err = agentBuilder.UploadLocalFile("4554", "./files/test.pdf")

	// 检查 err 是否为空，并且确保返回的错误信息包含 "id" 这个字段
	if err == nil || !strings.Contains(err.Error(), "body") || !strings.Contains(err.Error(), "id") {
		
	}
}
func TestNewAgentBuilderRunError(t *testing.T) {
	t.Parallel() // 并发运行
	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	agentBuilder, err := NewAgentBuilder(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AgentBuilder instance failed")
	}

	//测试1   conversationID为空
	_, err = agentBuilder.Run("", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Errorf("expected conversationID mustn't be empty, got %v", err)
	}

	//测试2   ServiceURLV2 error 无效的ServiceURLV2
	agentBuilder.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = agentBuilder.Run("2135", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}
	//测试3   t.client.Do 错误
	agentBuilder.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = agentBuilder.Run("1221", "描述简历中的候选人情况", nil, true)
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected Bad Request error, got %v", err)
	}
}
func TestNewAgentBuilder(t *testing.T) {
	// 创建缓冲区来存储日志
	var logBuffer bytes.Buffer

	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")

	// 将日志输出重定向到缓冲区
	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}
	// 测试逻辑
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "aa8af334-df27-4855-b3d1-0d249c61fc08"
	agentBuilder, err := NewAgentBuilder(appID, config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new AgentBuilder instance failed")
	}

	//正常测试
	conversationID, err := agentBuilder.CreateConversation()
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create conversation failed: %v", err)
	}
	_, err = agentBuilder.UploadLocalFile(conversationID, "./files/test.pdf")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upload local file failed: %v", err)
	}
	i, err := agentBuilder.Run(conversationID, "描述简历中的候选人情况", nil, true)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run failed:%v", err)
	}
	totalAnswer := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			switch ev.ContentType {
			case TextContentType:
				detail := ev.Detail.(TextDetail)
				log("---------------TextDetail------------")
				log("%v", detail)
			case CodeContentType:
				detail := ev.Detail.(CodeDetail)
				log("---------------CodeDetail------------")
				log("%v", detail)
			case ImageContentType:
				detail := ev.Detail.(ImageDetail)
				log("---------------ImageDetail------------")
				log("%v", detail)
			case RAGContentType:
				detail := ev.Detail.(RAGDetail)
				log("---------------RAGDetail------------")
				log("%v", detail)
			case FunctionCallContentType:
				detail := ev.Detail.(FunctionCallDetail)
				log("---------------FunctionCallDetail------------")
				log("%v", detail)
			case AudioContentType:
				detail := ev.Detail.(AudioDetail)
				log("---------------AudioDetail------------")
				log("%v", detail.Audio)
			case VideoContentType:
				detail := ev.Detail.(VideoDetail)
				log("---------------VideoDetail------------")
				log("%v", detail)
			case StatusContentType:
				// No additional detail to log
			default:
				// 默认是 json.RawMessage
				detail, ok := ev.Detail.(json.RawMessage)
				if !ok {
					t.Fatalf("unknown detail type")
				}
				log("---------------rawMessage------------")
				log("%s", string(detail))
			}
		}
	}
	log("----------------answer-------------------")
	log(totalAnswer)
	//测试4   非流式
	_, err = agentBuilder.Run(conversationID, "描述简历中的候选人情况", nil, false)
	if err != nil {

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
