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

func TestDataset(t *testing.T) {
	// 创建缓冲区来存储日志
	var logBuffer bytes.Buffer

	// 定义一个日志函数，将日志写入缓冲区
	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	// 测试逻辑
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}
	dataset, _ := NewDataset(config)
	datasetID, err := dataset.Create("测试集合")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create dataset failed: %v", err)
	}
	log("Dataset created with ID: %s", datasetID)

	documentID, err := dataset.UploadLocalFile(datasetID, "./files/test.pdf")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upload file failed: %v", err)
	}
	log("Document uploaded with ID: %s", documentID)

	_, err = dataset.ListDocument(datasetID, 1, 10, "")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("list document failed: %v", err)
	}
	log("Listed documents for dataset ID: %s", datasetID)

	if err := dataset.DeleteDocument(datasetID, documentID); err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("delete document failed: %v", err)
	}
	log("Document deleted with ID: %s", documentID)

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}