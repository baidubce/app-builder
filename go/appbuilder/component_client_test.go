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
	"fmt"
	"os"
	"testing"
)

func TestComponentClient(t *testing.T) {
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

	componentID := "44205c67-3980-41f7-aad4-37357b577fd0"
	client, err := NewComponentClient(config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new ComponentClient instance failed")
	}

	parameters := map[string]any{
		SysOriginQuery: "北京景点推荐",
	}
	i, err := client.Run(componentID, "latest", "", false, parameters)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run component failed: %v", err)
	}

	// test result
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		data := answer.Content[0].Text
		if data == nil {
			t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
			t.Fatalf("run component failed: data is nil")
		}
	}

	i2, err := client.Run(componentID, "latest", "", true, parameters)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run component failed: %v", err)
	}

	// test stream result
	var answerText any
	for answer, err := i2.Next(); err == nil; answer, err = i2.Next() {
		if len(answer.Content) == 0 {
			continue
		}
		answerText = answer.Content[0].Text
	}
	if answerText == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("run component failed: data is nil")
	}

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else { // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestComponentClientHeader(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	componentID := "c-wf-a39ee06c-808f-4a19-9f5f-544044283749"
	parameters := map[string]any{
		SysOriginQuery: "梦到巨人，是怎么回事",
	}
	componentClient, err := NewComponentClient(config)
	if err != nil {
		t.Error(err)
		return
	}

	ret, err := componentClient.Run(componentID, "latest", "", false, parameters)
	if err != nil {
		t.Error(err)
		return
	}

	for answer, err := ret.Next(); err == nil; answer, err = ret.Next() {
		t.Log(answer.Content[0].Text["info"])
	}

	ret2, err := componentClient.Run(componentID, "latest", "", true, parameters)
	if err != nil {
		t.Error(err)
		return
	}

	for answer, err := ret2.Next(); err == nil; answer, err = ret2.Next() {
		if len(answer.Content) == 0 {
			continue
		}
		t.Log(answer.Content[0].Text["info"])
	}

}
