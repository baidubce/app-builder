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
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

// Deprecated: 请使用AppBuilderClient 代替 AgentBuilder
func NewAgentBuilder(appID string, config *SDKConfig) (*AgentBuilder, error) {
	if len(appID) == 0 {
		return nil, errors.New("appID is empty")
	}
	if config == nil {
		return nil, errors.New("config is nil")
	}
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 300 * time.Second}
	}
	return &AgentBuilder{appID: appID, sdkConfig: config, client: client}, nil
}

type AgentBuilder struct {
	appID     string
	sdkConfig *SDKConfig
	client    HTTPClient
}

func (t *AgentBuilder) CreateConversation() (string, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/app/conversation")
	if err != nil {
		return "", err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	req := map[string]string{"app_id": t.appID}
	data, _ := json.Marshal(req)
	request.Body = io.NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := make(map[string]any)
	if err := json.Unmarshal(data, &rsp); err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	val, ok := rsp["conversation_id"]
	if !ok {
		return "", fmt.Errorf("requestID=%s, body=%s", requestID, string(data))
	}
	return val.(string), nil
}

func (t *AgentBuilder) UploadLocalFile(conversationID string, filePath string) (string, error) {
	var data bytes.Buffer
	w := multipart.NewWriter(&data)
	appIDPart, _ := w.CreateFormField("app_id")
	appIDPart.Write([]byte(t.appID))
	conversationIDPart, _ := w.CreateFormField("conversation_id")
	conversationIDPart.Write([]byte(conversationID))
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()
	filePart, _ := w.CreateFormFile("file", filepath.Base(filePath))
	if _, err := io.Copy(filePart, file); err != nil {
		return "", err
	}
	w.Close()
	request := http.Request{}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/app/conversation/file/upload")
	if err != nil {
		return "", err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header := t.sdkConfig.AuthHeaderV2()
	header.Set("Content-Type", w.FormDataContentType())
	request.Header = header
	request.Body = io.NopCloser(bytes.NewReader(data.Bytes()))
	resp, err := t.client.Do(&request)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := make(map[string]any)
	if err := json.Unmarshal(body, &rsp); err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	val, ok := rsp["id"]
	if !ok {
		return "", fmt.Errorf("requestID=%s, body=%s", requestID, string(body))
	}
	return val.(string), nil
}

func (t *AgentBuilder) Run(conversationID string, query string, fileIDS []string, stream bool) (AgentBuilderIterator, error) {
	if len(conversationID) == 0 {
		return nil, errors.New("conversationID mustn't be empty")
	}
	m := map[string]any{"app_id": t.appID,
		"conversation_id": conversationID,
		"query":           query,
		"file_ids":        fileIDS,
		"stream":          stream,
	}
	request := http.Request{}

	serviceURL, err := t.sdkConfig.ServiceURLV2("/app/conversation/runs")
	if err != nil {
		return nil, err
	}

	request.URL = serviceURL
	request.Method = "POST"
	header := t.sdkConfig.AuthHeaderV2()
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(m)
	request.Body = io.NopCloser(bytes.NewReader(data))
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
	if stream {
		return &AgentBuilderStreamIterator{requestID: requestID, r: r, body: resp.Body}, nil
	}
	return &AgentBuilderOnceIterator{body: resp.Body}, nil
}
