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
	"encoding/json"
	"fmt"
	"os"
	"testing"
)

func TestNewAgentBuilder(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	appID := ""
	agentBuilder, err := NewAgentBuilder(appID, config)
	if err != nil {
		t.Fatalf("new AgentBuidler instance failed")
	}
	conversationID, err := agentBuilder.CreateConversation()
	if err != nil {
		t.Fatalf("create conversation failed: %v", err)
	}
	_, err = agentBuilder.UploadLocalFile(conversationID, "./files/test.pdf")
	if err != nil {
		t.Fatalf("upload local file failed: %v", err)
	}
	i, err := agentBuilder.Run(conversationID, "描述简历中的候选人情况", nil, true)
	if err != nil {
		t.Fatalf("run failed:%v", err)
	}
	totalAnswer := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			if ev.ContentType == TextContentType {
				detail := ev.Detail.(TextDetail)
				fmt.Println("---------------TextDetail------------")
				fmt.Println(detail)
			} else if ev.ContentType == CodeContentType {
				detail := ev.Detail.(CodeDetail)
				fmt.Println("---------------CodeDetail------------")
				fmt.Println(detail)
			} else if ev.ContentType == ImageContentType {
				detail := ev.Detail.(ImageDetail)
				fmt.Println("---------------ImageDetail------------")
				fmt.Println(detail)
			} else if ev.ContentType == RAGContentType {
				detail := ev.Detail.(RAGDetail)
				fmt.Println("---------------RAGDetail------------")
				fmt.Println(detail)
			} else if ev.ContentType == FunctionCallContentType {
				detail := ev.Detail.(FunctionCallDetail)
				fmt.Println("---------------FunctionCallDetail------------")
				fmt.Println(detail)
			} else if ev.ContentType == AudioContentType {
				fmt.Println("---------------AudioDetail------------")
				detail := ev.Detail.(AudioDetail)
				fmt.Println(detail.Audio)
			} else if ev.ContentType == VideoContentType {
				fmt.Println("---------------VideoDetail------------")
				detail := ev.Detail.(VideoDetail)
				fmt.Println(detail)
			} else if ev.ContentType == StatusContentType {
			} else { // 默认是json.RawMessage
				detail, ok := ev.Detail.(json.RawMessage)
				if !ok {
					t.Fatalf("unknown detail type")
				}
				fmt.Println("---------------rawMessage------------")
				fmt.Println(string(detail))
			}
		}
	}
	fmt.Println("----------------answer-------------------")
	fmt.Println(totalAnswer)
}
