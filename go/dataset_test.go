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
	"testing"
)

func TestDataset(t *testing.T) {
	os.Setenv("APPBUILDER_TOKEN", "bce-v3/ALTAK-hB90vKrJc1RmeYuHw3zIG/4cf7ee64d6d055515473ca9ea66e0c29c52ee43e")
	os.Setenv("GATEWAY_URL", "http://10.153.106.18:8093")

	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	dataset, _ := NewDataset(config)
	datasetID, err := dataset.Create("测试集合")
	if err != nil {
		t.Fatalf("create dataset failed: %v", err)
	}
	documentID, err := dataset.UploadLocalFile(datasetID, "/Users/zhangxiaoyu15/Desktop/cv.pdf")
	if err != nil {
		t.Fatalf("upload file failed: %v", err)
	}
	_, err = dataset.ListDocument(datasetID, 1, 10, "")
	if err != nil {
		t.Fatalf("list document failed: %v", err)
	}
	if err := dataset.DeleteDocument(datasetID, documentID); err != nil {
		t.Fatalf("delet documeny failed: %v", err)
	}
}
