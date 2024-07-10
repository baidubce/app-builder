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
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strconv"
	"time"
)

func NewKnowledgeBase(config *SDKConfig) (*KnowledgeBase, error) {
	if config == nil {
		return nil, errors.New("invalid config")
	}
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 60 * time.Second}
	}
	return &KnowledgeBase{sdkConfig: config, client: client}, nil
}

type KnowledgeBase struct {
	sdkConfig *SDKConfig
	client    HTTPClient
}

func (t *KnowledgeBase) CreateDocument(req CreateDocumentRequest) (CreateDocumentResponse, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledge_base/document")
	if err != nil {
		return CreateDocumentResponse{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = io.NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return CreateDocumentResponse{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return CreateDocumentResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return CreateDocumentResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := CreateDocumentResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return CreateDocumentResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != "" {
		return CreateDocumentResponse{}, fmt.Errorf("requestID=%s, code=%s, message=%s", requestID, rsp.Code, rsp.Message)
	}
	return rsp, nil
}

func (t *KnowledgeBase) DeleteDocument(req DeleteDocumentRequest) error {
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledge_base/document")
	if err != nil {
		return err
	}

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

	request := http.Request{}
	request.URL = serviceURL
	request.Method = "DELETE"
	header.Set("Content-Type", "application/json")
	request.Header = header
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := http.DefaultClient.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	return nil
}

func (t *KnowledgeBase) GetDocumentList(req GetDocumentListRequest) (*GetDocumentListResponse, error) {
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledge_base/documents")
	if err != nil {
		return nil, err
	}

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

	request := http.Request{}
	request.URL = serviceURL
	request.Method = "GET"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = io.NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	respData, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := GetDocumentListResponse{}
	if err := json.Unmarshal(respData, &rsp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != "" {
		return nil, fmt.Errorf("requestID=%s, content=%s", requestID, string(respData))
	}
	return &rsp, nil
}

func (t *KnowledgeBase) UploadFile(localFilePath string) (string, error) {
	var data bytes.Buffer
	w := multipart.NewWriter(&data)
	file, err := os.Open(localFilePath)
	if err != nil {
		return "", err
	}
	defer file.Close()
	filePart, _ := w.CreateFormFile("file", filepath.Base(file.Name()))
	if _, err := io.Copy(filePart, file); err != nil {
		return "", err
	}
	w.Close()

	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/file")
	if err != nil {
		return "", err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", w.FormDataContentType())
	request.Header = header
	request.Body = io.NopCloser(bytes.NewReader(data.Bytes()))
	resp, err := t.client.Do(&request)
	if err != nil {
		return "", err
	}
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	respData, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := UploadFileResponse{}
	if err := json.Unmarshal(respData, &rsp); err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != "" {
		return "", fmt.Errorf("requestID=%s, content=%s", requestID, string(respData))
	}
	fileID := rsp.FileID
	return fileID, nil
}
