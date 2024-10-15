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
	"os"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"testing"
)
func TestNewRAGError(t *testing.T) {
	t.Parallel() // 并发运行
	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")

	// 测试逻辑
	config, err := NewSDKConfig("", "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "06e3f5c9-885d-4f85-af57-97dc85ee4606"

	// NewRAG测试 1: appID 为空，预期返回错误
	_, err = NewRAG("", &SDKConfig{})
	if err == nil || err.Error() != "appID is empty" {

	}

	// NewRAG测试 2: config 为 nil，预期返回错误
	_, err = NewRAG("validAppID", nil)
	if err == nil || err.Error() != "config is nil" {

	}
	//RAG测试
	rag, err := NewRAG(appID, config)
	if err != nil {

	}

	// CreateConversation测试 1: ServiceURLV2 错误
	rag.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = rag.Run("", "北京有多少小学生", true)
	if err == nil {

	}

	// CreateConversation测试 2: HTTP client do error
	rag.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = rag.Run("", "北京有多少小学生", true)
	if err == nil {

	}

	// CreateConversation测试 3: checkHTTPResponse 400 错误
	rag.client = &MockHTTPClient{}
	_, err = rag.Run("", "北京有多少小学生", true)
	if err == nil {

	}

	// CreateConversation测试 4: 非流式运行
	rag.client = &FaultyHTTPClient{}
	_, err = rag.Run("", "北京有多少小学生", false)
	if err == nil {

	}
}
func TestNewRAG(t *testing.T) {
	t.Parallel() // 并发运行
	// 设置环境变量
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")

	// 测试逻辑
	config, err := NewSDKConfig("", "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := "06e3f5c9-885d-4f85-af57-97dc85ee4606"

	//RAG测试
	rag, err := NewRAG(appID, config)
	if err != nil {
		t.Fatalf("new RAG instance failed")
	}
	fmt.Println("问题出现在这里2")

	i, err := rag.Run("", "北京有多少小学生", true)
	var answer *RAGAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		data, _ := json.Marshal(answer)
		fmt.Println(string(data))
		fmt.Println(answer.ConversationID)
	}
	if !errors.Is(err, io.EOF) {
		fmt.Println(err)
	}
}
