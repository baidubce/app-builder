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
	"bufio"
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strings"
	"time"
)

type ComponentClient struct {
	sdkConfig *SDKConfig
	client    HTTPClient
}

func NewComponentClient(config *SDKConfig) (*ComponentClient, error) {
	if config == nil {
		return nil, errors.New("config is nil")
	}
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 300 * time.Second}
	}
	return &ComponentClient{sdkConfig: config, client: client}, nil
}

func (t *ComponentClient) Run(component, version, action string, stream bool, parameters map[string]any) (ComponentClientIterator, error) {
	request := http.Request{}

	urlSuffix := fmt.Sprintf("/components/%s", component)
	if version != "" {
		urlSuffix += fmt.Sprintf("/version/%s", version)
	}
	if action != "" {
		if strings.Contains(urlSuffix, "?") {
			urlSuffix += fmt.Sprintf("&action=%s", action)
		} else {
			urlSuffix += fmt.Sprintf("?action=%s", action)
		}
	}

	serviceURL, err := t.sdkConfig.ServiceURLV2(urlSuffix)
	if err != nil {
		return nil, err
	}

	header := t.sdkConfig.AuthHeaderV2()
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	header.Set("X-Appbuilder-From", "sdk")
	request.Header = header

	req := ComponentRunRequest{
		Stream:     stream,
		Parameters: parameters,
	}
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	request.ContentLength = int64(len(data)) // 手动设置长度

	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return nil, err
	}
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	r := NewSSEReader(1024*1024, bufio.NewReader(resp.Body))
	if req.Stream {
		return &ComponentClientStreamIterator{requestID: requestID, r: r, body: resp.Body}, nil
	}
	return &ComponentClientOnceIterator{body: resp.Body}, nil
}
