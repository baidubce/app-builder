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

func TestNewAppBuilderClient2(t *testing.T) {
	    // 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取
		os.Setenv("APPBUILDER_TOKEN", "bce-v3/ALTAK-TnXvQ6z8XCvkZTzP5ShMP/fbd28a8e80f8c3fa1ad9d505db4f843c913858f9")
		// 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
		appID := "bc78732b-b6a6-474b-b2f8-475f60759426"
		config, err := appbuilder.NewSDKConfig("", "")
		if err != nil {
			fmt.Println("new config failed: ", err)
			return
		}
	
		builder, err := appbuilder.NewAppBuilderClient(appID, config)
		if err != nil {
			fmt.Println("new agent builder failed: ", err)
			return
		}
		conversationID, err := builder.CreateConversation()
		if err != nil {
			fmt.Println("create conversation failed: ", err)
			return
		}
	
		i, err := builder.Run(conversationID, "你好，你能做什么？", nil, false)
		if err != nil {
			fmt.Println("run failed: ", err)
			return
		}
	
		var answer *appbuilder.AppBuilderClientAnswer
		for answer, err = i.Next(); err == nil; answer, err = i.Next() {
			fmt.Println(answer.Answer)
		}
}
