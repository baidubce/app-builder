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
	"os"
	"path/filepath"
	"time"
)

// Deprecated: 已废弃，请使用 NewKnowledgeBase
func NewDataset(config *SDKConfig) (*Dataset, error) {
	if config == nil {
		return nil, errors.New("invalid config")
	}
	client := config.HTTPClient
	if client == nil {
		client = &http.Client{Timeout: 60 * time.Second}
	}
	return &Dataset{sdkConfig: config, client: client}, nil
}

type Dataset struct {
	sdkConfig *SDKConfig
	client    HTTPClient
}

func (t *Dataset) Create(name string) (string, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeader()
	serviceURL, err := t.sdkConfig.ServiceURL("/api/v1/ai_engine/agi_platform/v1/datasets/create")
	if err != nil {
		return "", err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	req := map[string]string{"name": name}
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
	rsp := DatasetResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != 0 {
		return "", fmt.Errorf("requestID=%s, content=%v", requestID, string(data))
	}
	return rsp.Result["id"].(string), nil
}

func (t *Dataset) BatchUploadLocaleFile(datasetID string, localFilePaths []string) ([]string, error) {
	var fileIDs []string
	for _, localFilePath := range localFilePaths {
		fileID, err := t.uploadLocalFile(localFilePath)
		if err != nil {
			return nil, err
		}
		fileIDs = append(fileIDs, fileID)
	}
	documentIDS, err := t.addFileToDataset(datasetID, fileIDs)
	if err != nil {
		return nil, err
	}
	return documentIDS, nil
}

func (t *Dataset) UploadLocalFile(datasetID string, localFilePath string) (string, error) {
	fileID, err := t.uploadLocalFile(localFilePath)
	if err != nil {
		return "", err
	}
	documentIDs, err := t.addFileToDataset(datasetID, []string{fileID})
	if err != nil {
		return "", fmt.Errorf("add file failed: %v", err)
	}
	return documentIDs[0], nil
}

func (t *Dataset) uploadLocalFile(localFilePath string) (string, error) {
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
	header := t.sdkConfig.AuthHeader()
	serviceURL, err := t.sdkConfig.ServiceURL("/api/v1/ai_engine/agi_platform/v1/datasets/files/upload")
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
	rsp := DatasetResponse{}
	if err := json.Unmarshal(respData, &rsp); err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != 0 {
		return "", fmt.Errorf("requestID=%s, content=%s", requestID, string(respData))
	}
	fileID := rsp.Result["id"].(string)
	return fileID, nil
}

func (t *Dataset) addFileToDataset(datasetID string, fileID []string) ([]string, error) {
	header := t.sdkConfig.AuthHeader()
	serviceURL, err := t.sdkConfig.ServiceURL("/api/v1/ai_engine/agi_platform/v1/datasets/documents")
	if err != nil {
		return nil, err
	}
	request := http.Request{}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	m := map[string]any{
		"file_ids":   fileID,
		"dataset_id": datasetID}
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
	respData, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := DatasetBindResponse{}
	if err := json.Unmarshal(respData, &rsp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != 0 {
		return nil, fmt.Errorf("requestID=%s, content=%s", requestID, string(respData))
	}
	return rsp.Result.DocumentIDs, nil
}

func (t *Dataset) ListDocument(datasetID string, page int, limit int, keyword string) (*ListDocumentResponse, error) {
	header := t.sdkConfig.AuthHeader()
	serviceURL, err := t.sdkConfig.ServiceURL("/api/v1/ai_engine/agi_platform/v1/datasets/documents/list_page")
	if err != nil {
		return nil, err
	}
	request := http.Request{}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	m := map[string]any{
		"dataset_id": datasetID,
		"page":       page,
		"limit":      limit,
		"keyword":    keyword,
	}
	data, _ := json.Marshal(m)
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
	rsp := ListDocumentResponse{}
	if err := json.Unmarshal(respData, &rsp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	if rsp.Code != 0 {
		return nil, fmt.Errorf("requestID=%s, content=%s", requestID, string(respData))
	}
	return &rsp, nil
}

func (t *Dataset) DeleteDocument(datasetID, documentID string) error {
	fmt.Println(datasetID, "  ", documentID)
	header := t.sdkConfig.AuthHeader()
	serviceURL, err := t.sdkConfig.ServiceURL("/api/v1/ai_engine/agi_platform/v1/datasets/document/delete")
	if err != nil {
		return err
	}
	request := http.Request{}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	m := map[string]string{
		"dataset_id":  datasetID,
		"document_id": documentID,
	}
	data, _ := json.Marshal(m)
	request.Body = io.NopCloser(bytes.NewReader(data))
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
