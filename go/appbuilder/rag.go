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
	"io"
	"net/http"

	"github.com/baidubce/app-builder/go/appbuilder/internal/parser"
)

func NewRAG(appID string, config *SDKConfig) (*RAG, error) {
	if len(appID) == 0 {
		return nil, fmt.Errorf("appID is empty")
	}
	if config == nil {
		return nil, fmt.Errorf("invalid config")
	}
	return &RAG{appID: appID, sdkConfig: config}, nil
}

type RAG struct {
	appID     string
	sdkConfig *SDKConfig
}

func (t *RAG) Run(conversationID string, query string, stream bool) (RAGIterator, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeader()
	serviceURL, err := t.sdkConfig.ServiceURL("/api/v1/ai_engine/agi_platform/ai_apaas/v1/instance/integrated")
	if err != nil {
		return nil, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	req := map[string]string{"conversation_id": conversationID,
		"response_mode": "blocking",
		"query":         query,
		"app_id":        t.appID,
	}
	if stream {
		req["response_mode"] = "streaming"
	}
	data, _ := json.Marshal(req)
	request.Body = io.NopCloser(bytes.NewReader(data))
	resp, err := http.DefaultClient.Do(&request)
	if err != nil {
		return nil, err
	}
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if stream {
		return &RAGStreamIterator{p: parser.New(resp.Body), requestID: requestID}, nil
	} else {
		return &RAGOnceIterator{body: resp.Body}, nil
	}
}
