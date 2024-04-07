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
	"fmt"
	"os"
	"testing"
)

func TestNewRAG(t *testing.T) {
	os.Setenv("GATEWAY_URL", "bce-v3/ALTAK-hB90vKrJc1RmeYuHw3zIG/4cf7ee64d6d055515473ca9ea66e0c29c52ee43e")
	os.Setenv("APPBUILDER_TOKEN", "https://apaas-api-sandbox.baidu-int.com")
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}
	rag, err := NewRAG("a2c21aa5-bb5e-4e2f-b1b2-2321a806496b", config)
	if err != nil {
		t.Fatalf("new AgentBuidler instance failed")
	}
	i, err := rag.Run("ed44dbcc-cd1f-4215-960c-cf599adecfe0", "面试需要注意的细节", true)
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		fmt.Println(answer.Answer)
	}
}
