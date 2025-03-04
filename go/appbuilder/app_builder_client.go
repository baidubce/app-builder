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
	"net/url"
	"os"
	"path/filepath"
	"reflect"
	"strconv"
	"time"
)

// Deprecated: 将废弃，请使用DescribeApps替代
func GetAppList(req GetAppListRequest, config *SDKConfig) ([]App, error) {
	request := http.Request{}
	header := config.AuthHeaderV2()
	serviceURL, err := config.ServiceURLV2("/apps")
	if err != nil {
		return nil, err
	}

	request.URL = serviceURL
	request.Method = "GET"
	header.Set("Content-Type", "application/json")
	request.Header = header

	reqMap := make(map[string]any)
	reqJson, _ := json.Marshal(req)
	json.Unmarshal(reqJson, &reqMap)
	params := url.Values{}
	for key, value := range reqMap {
		switch v := value.(type) {
		case float64:
			params.Add(key, strconv.Itoa(int(v)))
		case string:
			if v == "" {
				continue
			}
			params.Add(key, v)
		}
	}
	serviceURL.RawQuery = params.Encode()

	config.BuildCurlCommand(&request)
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 300 * time.Second}
	}
	resp, err := client.Do(&request)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := GetAppListResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp.Data, nil
}

func DescribeApps(req DescribeAppsRequest, config *SDKConfig) (DescribeAppsResponse, error) {
	request := http.Request{}
	header := config.AuthHeaderV2()
	serviceURL, err := config.ServiceURLV2("/app?Action=DescribeApps")
	if err != nil {
		return DescribeAppsResponse{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	config.BuildCurlCommand(&request)
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 300 * time.Second}
	}
	resp, err := client.Do(&request)
	if err != nil {
		return DescribeAppsResponse{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return DescribeAppsResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return DescribeAppsResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := DescribeAppsResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return DescribeAppsResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp, nil
}

func NewAppBuilderClient(appID string, config *SDKConfig) (*AppBuilderClient, error) {
	if appID == "" {
		return nil, errors.New("appID is empty")
	}
	if config == nil {
		return nil, errors.New("config is nil")
	}
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 300 * time.Second}
	}
	return &AppBuilderClient{appID: appID, sdkConfig: config, client: client}, nil
}

type AppBuilderClient struct {
	appID     string
	sdkConfig *SDKConfig
	client    HTTPClient
}

// 在 AppBuilderClient 结构体中添加 Getter 方法
func (t *AppBuilderClient) GetSdkConfig() *SDKConfig {
	return t.sdkConfig
}

func (t *AppBuilderClient) GetClient() HTTPClient {
	return t.client
}

type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

func (t *AppBuilderClient) CreateConversation() (string, error) {
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

func (t *AppBuilderClient) UploadLocalFile(conversationID string, filePath string) (string, error) {
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
	request.Body = NopCloser(bytes.NewReader(data.Bytes()))
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

func (t *AppBuilderClient) UploadFile(req *AppBuilderClientUploadFileRequest) (string, error) {
	var appID string
	if req.AppID != "" {
		appID = req.AppID
	} else {
		appID = t.appID
	}
	if appID == "" {
		return "", errors.New("appID is required")
	}
	if req.FilePath == "" && req.FileURL == "" {
		return "", errors.New("either FilePath or FileURL is required")
	}

	var data bytes.Buffer
	w := multipart.NewWriter(&data)
	appIDPart, _ := w.CreateFormField("app_id")
	appIDPart.Write([]byte(appID))
	conversationIDPart, _ := w.CreateFormField("conversation_id")
	conversationIDPart.Write([]byte(req.ConversationID))
	if req.FilePath != "" {
		file, err := os.Open(req.FilePath)
		if err != nil {
			return "", err
		}
		defer file.Close()
		filePart, _ := w.CreateFormFile("file", filepath.Base(req.FilePath))
		if _, err := io.Copy(filePart, file); err != nil {
			return "", err
		}
	} else {
		fileURLPart, _ := w.CreateFormField("file_url")
		fileURLPart.Write([]byte(req.FileURL))
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
	request.Body = NopCloser(bytes.NewReader(data.Bytes()))
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

func (t *AppBuilderClient) Run(param ...interface{}) (AppBuilderClientIterator, error) {
	if len(param) == 0 {
		return nil, errors.New("no arguments provided")
	}
	var err error
	var req AppBuilderClientRunRequest

	if reflect.TypeOf(param[0]) == reflect.TypeOf(AppBuilderClientRunRequest{}) {
		req = param[0].(AppBuilderClientRunRequest)
	} else {
		req, err = t.buildAppBuilderClientRunRequest(param...)
		if err != nil {
			return nil, err
		}
	}

	if len(req.ConversationID) == 0 {
		return nil, errors.New("conversationID mustn't be empty")
	}

	if len(req.AppID) == 0 {
		req.AppID = t.appID
	}

	request := http.Request{}

	serviceURL, err := t.sdkConfig.ServiceURLV2("/app/conversation/runs")
	if err != nil {
		return nil, err
	}

	header := t.sdkConfig.AuthHeaderV2()
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	request.ContentLength = int64(len(data))

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
		return &AppBuilderClientStreamIterator{requestID: requestID, r: r, body: resp.Body}, nil
	}
	return &AppBuilderClientOnceIterator{body: resp.Body}, nil
}

func (t *AppBuilderClient) buildAppBuilderClientRunRequest(param ...interface{}) (AppBuilderClientRunRequest, error) {
	conversationID, ok := param[0].(string)
	if !ok {
		return AppBuilderClientRunRequest{}, errors.New("conversationID must be string type")
	}
	query, ok := param[1].(string)
	if !ok {
		return AppBuilderClientRunRequest{}, errors.New("query must be string type")
	}

	var fileIDS []string
	if param[2] != nil {
		fileIDS, ok = param[2].([]string)
		if !ok {
			fileIDS = nil
		}
	}

	stream, ok := param[3].(bool)
	if !ok {
		stream = false
	}

	return AppBuilderClientRunRequest{
		AppID:          t.appID,
		ConversationID: conversationID,
		Query:          query,
		Stream:         stream,
		FileIDs:        fileIDS,
	}, nil
}

func (t *AppBuilderClient) Feedback(req AppBuilderClientFeedbackRequest) (string, error) {
	if len(req.ConversationID) == 0 {
		return "", errors.New("conversationID mustn't be empty")
	}

	if len(req.AppID) == 0 {
		req.AppID = t.appID
	}

	request := http.Request{}

	serviceURL, err := t.sdkConfig.ServiceURLV2("/app/conversation/feedback")
	if err != nil {
		return "", err
	}

	header := t.sdkConfig.AuthHeaderV2()
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	request.ContentLength = int64(len(data)) // 手动设置长度

	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return "", err
	}
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return requestID, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	return requestID, nil
}

// Deprecated: Run方法已兼容此方法
func (t *AppBuilderClient) RunWithToolCall(req AppBuilderClientRunRequest) (AppBuilderClientIterator, error) {
	if len(req.ConversationID) == 0 {
		return nil, errors.New("conversationID mustn't be empty")
	}

	request := http.Request{}

	serviceURL, err := t.sdkConfig.ServiceURLV2("/app/conversation/runs")
	if err != nil {
		return nil, err
	}

	header := t.sdkConfig.AuthHeaderV2()
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
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
		return &AppBuilderClientStreamIterator{requestID: requestID, r: r, body: resp.Body}, nil
	}
	return &AppBuilderClientOnceIterator{body: resp.Body}, nil
}
