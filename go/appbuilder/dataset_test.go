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
	// "bytes"
	// "fmt"
	"os"
	"testing"
)

func TestDatasetError(t *testing.T) {
	t.Parallel() // 并发运行
	// 测试逻辑
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	var GatewayURL = config.GatewayURLV2

	dataset, _ := NewDataset(config)

	//dataset.Create测试1 无效的ServiceURLV2
	dataset.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = dataset.Create("测试集合")
	if err == nil {

	}

	// 测试 UploadLocalFile 2: t.client.Do 错误
	dataset.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = dataset.Create("测试集合")
	if err == nil {

	}

	// 测试 UploadLocalFile 4: 错误的 HTTP 响应
	dataset.client = &MockHTTPClient{}
	dataset.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = dataset.Create("测试集合")
	if err == nil {

	}
	// 测试 UploadLocalFile 5: 模拟读取 body 时发生错误
	dataset.client = &FaultyHTTPClient{}
	dataset.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = dataset.Create("测试集合")
	if err == nil {

	}

	//NewDataset测试1 config == nil
	dataset, _ = NewDataset(nil)
	//NewDataset测试2 client == nil
	config.HTTPClient = nil
	dataset, _ = NewDataset(config)

}
// func TestDataset(t *testing.T) {
// 	t.Parallel() // 并发运行
// 	// 创建缓冲区来存储日志
// 	var logBuffer bytes.Buffer

// 	// 定义一个日志函数，将日志写入缓冲区
// 	log := func(format string, args ...interface{}) {
// 		fmt.Fprintf(&logBuffer, format+"\n", args...)
// 	}

// 	// 测试逻辑
// 	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
// 	if err != nil {
// 		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
// 		t.Fatalf("new http client config failed: %v", err)
// 	}
// 	dataset, _ := NewDataset(config)
// 	datasetID, err := dataset.Create("测试集合")
// 	if err != nil {
// 		datasetID = os.Getenv(SecretKeyV3)
// 	}

// 	_, err = dataset.ListDocument(datasetID, 1, 10, "")
// 	if err != nil {
// 		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
// 		t.Fatalf("list document failed: %v", err)
// 	}
// 	log("Listed documents for dataset ID: %s", datasetID)

// 	// 如果测试失败，则输出缓冲区中的日志
// 	if t.Failed() {
// 		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
// 		fmt.Println(logBuffer.String())
// 	} else { // else 紧跟在右大括号后面
// 		// 测试通过，打印文件名和测试函数名
// 		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
// 	}
// }
