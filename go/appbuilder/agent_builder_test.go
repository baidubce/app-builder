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

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}
