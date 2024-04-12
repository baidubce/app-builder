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
	"errors"
	"fmt"
	"io"
	"testing"
)

func TestNewRAG(t *testing.T) {
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	rag, err := NewRAG("", config)
	if err != nil {
		t.Fatalf("new RAG instance failed")
	}
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
