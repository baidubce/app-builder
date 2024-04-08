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
	"testing"
)

func TestDataset(t *testing.T) {
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	dataset, _ := NewDataset(config)
	datasetID, err := dataset.Create("测试集合")
	if err != nil {
		t.Fatalf("create dataset failed: %v", err)
	}
	documentID, err := dataset.UploadLocalFile(datasetID, "/path/to/cv.pdf")
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
