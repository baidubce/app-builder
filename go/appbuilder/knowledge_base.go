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

	"github.com/google/uuid"
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
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}

	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledge_base/document?clientToken=" + req.ClientToken)
	if err != nil {
		return CreateDocumentResponse{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
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
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledge_base/document?clientToken=" + req.ClientToken)
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
	request.Body = NopCloser(bytes.NewReader(data))
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
	request.Body = NopCloser(bytes.NewReader(data.Bytes()))
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

func (t *KnowledgeBase) CreateKnowledgeBase(req KnowledgeBaseDetail) (KnowledgeBaseDetail, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=CreateKnowledgeBase&clientToken=" + req.ClientToken)
	if err != nil {
		return KnowledgeBaseDetail{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return KnowledgeBaseDetail{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return KnowledgeBaseDetail{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return KnowledgeBaseDetail{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := KnowledgeBaseDetail{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return KnowledgeBaseDetail{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp, nil
}

func (t *KnowledgeBase) GetKnowledgeBaseDetail(knowledgeBaseID string) (KnowledgeBaseDetail, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=DescribeKnowledgeBase")
	if err != nil {
		return KnowledgeBaseDetail{}, err
	}
	req := KnowledgeBaseDetail{}
	req.ID = knowledgeBaseID
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return KnowledgeBaseDetail{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return KnowledgeBaseDetail{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return KnowledgeBaseDetail{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := KnowledgeBaseDetail{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return KnowledgeBaseDetail{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp, nil
}

func (t *KnowledgeBase) GetKnowledgeBaseList(req GetKnowledgeBaseListRequest) (GetKnowledgeBaseListResponse, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=DescribeKnowledgeBases")
	if err != nil {
		return GetKnowledgeBaseListResponse{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return GetKnowledgeBaseListResponse{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return GetKnowledgeBaseListResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return GetKnowledgeBaseListResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	rsp := GetKnowledgeBaseListResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return GetKnowledgeBaseListResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp, nil
}

func (t *KnowledgeBase) ModifyKnowledgeBase(req ModifyKnowlegeBaseRequest) error {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=ModifyKnowledgeBase&clientToken=" + req.ClientToken)
	if err != nil {
		return err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	_, err = io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return nil
}

func (t *KnowledgeBase) DeleteKnowledgeBase(knowledgeBaseID string) error {
	return t.deleteKnowledgeBase(knowledgeBaseID, "")
}

func (t *KnowledgeBase) DeleteKnowledgeBaseWithReq(req DeleteKnowlegeBaseRequest) error {
	return t.deleteKnowledgeBase(req.ID, req.ClientToken)
}

func (t *KnowledgeBase) deleteKnowledgeBase(knowledgeBaseID string, clientToken string) error {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if clientToken == "" {
		clientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=DeleteKnowledgeBase&clientToken=" + clientToken)
	if err != nil {
		return err
	}
	req := KnowledgeBaseDetail{}
	req.ID = knowledgeBaseID
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	_, err = io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return nil
}

func (t *KnowledgeBase) CreateDocuments(req CreateDocumentsRequest) error {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=CreateDocuments&clientToken=" + req.ClientToken)
	if err != nil {
		return err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	_, err = io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return nil
}

func (t *KnowledgeBase) UploadDocuments(localFilePath string, req CreateDocumentsRequest) error {
	var data bytes.Buffer
	w := multipart.NewWriter(&data)
	file, err := os.Open(localFilePath)
	if err != nil {
		return err
	}
	defer file.Close()
	filePart, _ := w.CreateFormFile("file", filepath.Base(file.Name()))
	if _, err := io.Copy(filePart, file); err != nil {
		return err
	}

	jsonData, err := json.Marshal(req)
	if err != nil {
		return fmt.Errorf("failed to marshal request: %w", err)
	}
	jsonPart, err := w.CreateFormField("payload")
	if err != nil {
		return fmt.Errorf("failed to create form field: %w", err)
	}
	if _, err := jsonPart.Write(jsonData); err != nil {
		return fmt.Errorf("failed to write JSON data: %w", err)
	}
	w.Close()

	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=UploadDocuments&clientToken=" + req.ClientToken)
	if err != nil {
		return err
	}
	request.URL = serviceURL
	request.Method = "POST"
	request.Header = header
	header.Set("Content-Type", w.FormDataContentType())
	request.Body = NopCloser(bytes.NewReader(data.Bytes()))
	resp, err := t.client.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	_, err = io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return nil
}

func (t *KnowledgeBase) CreateChunk(req CreateChunkRequest) (string, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=CreateChunk&clientToken=" + req.ClientToken)
	if err != nil {
		return "", err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
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

	rsp := CreateChunkResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return "", fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp.ID, nil
}

func (t *KnowledgeBase) ModifyChunk(req ModifyChunkRequest) error {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if req.ClientToken == "" {
		req.ClientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=ModifyChunk&clientToken=" + req.ClientToken)
	if err != nil {
		return err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	rsp := CreateChunkResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return nil
}

func (t *KnowledgeBase) DeleteChunk(chunkID string) error {
	return t.deleteChunk(chunkID, "")
}

func (t *KnowledgeBase) DeleteChunkWithReq(req DeleteChunkRequest) error {
	return t.deleteChunk(req.ChunkID, req.ClientToken)
}

func (t *KnowledgeBase) deleteChunk(chunkID string, clientToken string) error {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	if clientToken == "" {
		clientToken = uuid.New().String()
	}
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=DeleteChunk&clientToken=" + clientToken)
	if err != nil {
		return err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	req := DeleteChunkRequest{
		ChunkID: chunkID,
	}
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	rsp := CreateChunkResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return nil
}

func (t *KnowledgeBase) DescribeChunk(chunkID string) (DescribeChunkResponse, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=DescribeChunk")
	if err != nil {
		return DescribeChunkResponse{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	req := DescribeChunkRequest{
		ChunkID: chunkID,
	}
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return DescribeChunkResponse{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return DescribeChunkResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return DescribeChunkResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	rsp := DescribeChunkResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return DescribeChunkResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp, nil
}

func (t *KnowledgeBase) DescribeChunks(req DescribeChunksRequest) (DescribeChunksResponse, error) {
	request := http.Request{}
	header := t.sdkConfig.AuthHeaderV2()
	serviceURL, err := t.sdkConfig.ServiceURLV2("/knowledgeBase?Action=DescribeChunks")
	if err != nil {
		return DescribeChunksResponse{}, err
	}
	request.URL = serviceURL
	request.Method = "POST"
	header.Set("Content-Type", "application/json")
	request.Header = header
	data, _ := json.Marshal(req)
	request.Body = NopCloser(bytes.NewReader(data))
	t.sdkConfig.BuildCurlCommand(&request)
	resp, err := t.client.Do(&request)
	if err != nil {
		return DescribeChunksResponse{}, err
	}
	defer resp.Body.Close()
	requestID, err := checkHTTPResponse(resp)
	if err != nil {
		return DescribeChunksResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}
	data, err = io.ReadAll(resp.Body)
	if err != nil {
		return DescribeChunksResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	rsp := DescribeChunksResponse{}
	if err := json.Unmarshal(data, &rsp); err != nil {
		return DescribeChunksResponse{}, fmt.Errorf("requestID=%s, err=%v", requestID, err)
	}

	return rsp, nil
}
