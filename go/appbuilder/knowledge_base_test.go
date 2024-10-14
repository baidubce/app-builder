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
	"fmt"
	"os"
	"testing"
	"time"
	"strings"
)
func TestAddDocumentError(t *testing.T) {
	t.Parallel() // 并发运行
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")
	//NewKnowledgeBase测试1 config== nil
	_, err := NewKnowledgeBase(nil)
	if err == nil {
		t.Errorf("expected config= nil error, got %v", err)
	}

	knowledgeBaseID := os.Getenv(DatasetIDV3)
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new Knowledge base instance failed")
	}

	var GatewayURL = client.sdkConfig.GatewayURLV2
	var clientT = client.client
	// 测试 UploadLocalFile 1: 文件打开错误
	_, err = client.UploadFile("invalidFilePath")
	if err == nil || !strings.Contains(err.Error(), "no such file or directory") {
		t.Errorf("expected file open error, got %v", err)
	}
	// 测试 UploadLocalFile 2: t.client.Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.UploadFile("./files/test.pdf")
	if err == nil {
		t.Errorf("expected client error, got nil")
	}

	// 测试 UploadLocalFile 3: 无效的ServiceURLV2
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.UploadFile("./files/test.pdf")
	if err == nil || !strings.Contains(err.Error(), "missing protocol scheme") {
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}

	// 测试 UploadLocalFile 4: 错误的 HTTP 响应
	client.client = &MockHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadFile("./files/test.pdf")
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}
	// 测试 UploadLocalFile 5: 模拟读取 body 时发生错误
	client.client = &FaultyHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadFile("./files/test.pdf")
	if err == nil {
		t.Fatalf("expected read error, got nil")
	}
	// 测试 UploadLocalFile 6: json.Unmarshal错误
	client.client = &InvalidJSONHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadFile("./files/test.pdf")
	if err == nil {
		t.Fatalf("expected JSON unmarshal error, got nil")
	}
	// 测试 UploadLocalFile 7: 缺少 id 字段
	client.client = &MissingIDHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	_, err = client.UploadFile("./files/test.pdf")
	if err == nil {
	}

	//正常测试
	client.client = clientT
	client.sdkConfig.GatewayURLV2 = GatewayURL
	fileID, err := client.UploadFile("./files/test.pdf")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upload file failed: %v", err)
	}
	//CreateDocument 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected ServiceURLV2 error, got %v", err)
	}
	//CreateDocument 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Errorf("expected Bad Request error, got %v", err)
	}
	//CreateDocument 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err == nil {
		t.Fatalf("expected 400 error, got nil")
	}

	//CreateDocument 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err == nil {
		t.Fatalf("expected read error, got nil")
	}

	//CreateDocument 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err == nil {
		t.Fatalf("expected JSON unmarshal error, got nil")
	}
	//CreateDocument 测试 6: 缺少 id 字段
	client.client = &MissingIDHTTPClient{}
	_, err = client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	// 检查 err 是否为空，并且确保返回的错误信息包含 "id" 这个字段
	if err == nil {
	}
	//还原设置
	client.client = clientT
	client.sdkConfig.GatewayURLV2 = GatewayURL
	createDocumentRes, err := client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create document failed: %v", err)
	}

	//DeleteDocument 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      createDocumentRes.DocumentsIDS[0]})
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")

	}
	//DeleteDocument 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      createDocumentRes.DocumentsIDS[0]})
	if err == nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")

	}
	//DeleteDocument 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      createDocumentRes.DocumentsIDS[0]})
	if err == nil {

	}


	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {

	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名

	}
}

func TestCreateKnowledgeBaseError(t *testing.T) {
	t.Parallel() // 并发运行
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {

	}

	client, err := NewKnowledgeBase(config)
	if err != nil {

	}
	var GatewayURL = client.sdkConfig.GatewayURLV2
	var clientT = client.client
	//CreateKnowledgeBase 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err == nil {

	}
	//CreateKnowledgeBase 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err == nil {

	}
	//CreateKnowledgeBase 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err == nil {

	}

	//CreateKnowledgeBase 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err == nil {

	}

	//CreateDocument 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err == nil {

	}

	client.client = clientT
	// 成功 创建知识库
	createKnowledgeBaseRes, err := client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err != nil {

	}
	knowledgeBaseID := createKnowledgeBaseRes.ID
	client.client = clientT
	//GetKnowledgeBaseDetail 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err == nil {

	}
	//GetKnowledgeBaseDetail 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err == nil {

	}
	//GetKnowledgeBaseDetail 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err == nil {

	}
	//GetKnowledgeBaseDetail 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err == nil {

	}
	//GetKnowledgeBaseDetail 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err == nil {

	}
	client.client = clientT
	//GetKnowledgeBaseList 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err == nil {

	}
	//GetKnowledgeBaseList 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err == nil {

	}
	//GetKnowledgeBaseList 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err == nil {

	}

	//GetKnowledgeBaseList 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err == nil {

	}

	//GetKnowledgeBaseList 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err == nil {

	}
	client.client = clientT
	//导入知识库 测试1 
	//导入知识库 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.CreateDocuments(CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type:     "web",
			Urls:     []string{"https://baijiahao.baidu.com/s?id=1802527379394162441"},
			UrlDepth: 1,
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}
	//导入知识库 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.CreateDocuments(CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type:     "web",
			Urls:     []string{"https://baijiahao.baidu.com/s?id=1802527379394162441"},
			UrlDepth: 1,
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}
	//导入知识库 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	err = client.CreateDocuments(CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type:     "web",
			Urls:     []string{"https://baijiahao.baidu.com/s?id=1802527379394162441"},
			UrlDepth: 1,
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}

	//导入知识库 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	err = client.CreateDocuments(CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type:     "web",
			Urls:     []string{"https://baijiahao.baidu.com/s?id=1802527379394162441"},
			UrlDepth: 1,
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}
	client.client = clientT
	// 测试上传知识库文档 UploadDocuments 1: 文件打开错误
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil || !strings.Contains(err.Error(), "no such file or directory") {

	}
	// 测试上传知识库文档 UploadDocuments 2: t.client.Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}

	// 测试上传知识库文档 UploadDocuments 3: 无效的ServiceURLV2
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil || !strings.Contains(err.Error(), "missing protocol scheme") {

	}

	// 测试上传知识库文档 UploadDocuments 4: 错误的 HTTP 响应
	client.client = &MockHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}
	// 测试上传知识库文档 UploadDocuments 5: 模拟读取 body 时发生错误
	client.client = &FaultyHTTPClient{}
	client.sdkConfig.GatewayURLV2 = GatewayURL
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err == nil {

	}

	client.client = clientT
	name := "test-go"
	description := "22"
	//测试修改知识库 GetKnowledgeBaseDetail 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err == nil {

	}
	//测试修改知识库 GetKnowledgeBaseDetail 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err == nil {

	}
	//测试修改知识库 GetKnowledgeBaseDetail 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err == nil {

	}
	//测试修改知识库 GetKnowledgeBaseDetail 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err == nil {

	}
	
	client.client = clientT
	//测试删除知识库 GetKnowledgeBaseDetail 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err == nil {

	}
	//测试删除知识库 GetKnowledgeBaseDetail 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err == nil {

	}
	//测试删除知识库 GetKnowledgeBaseDetail 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err == nil {

	}
	//测试删除知识库 GetKnowledgeBaseDetail 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err == nil {

	}
	client.client = clientT
	//删除知识库
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err != nil {

	}
}
func TestChunkError(t *testing.T) {
	t.Parallel() // 并发运行
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")

	documentID := os.Getenv(DocumentIDV3)
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new Knowledge base instance failed")
	}
	var clientT = client.client 
	var GatewayURL = client.sdkConfig.GatewayURLV2

	//测试创建切片 CreateChunk 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err == nil {

	}
	//测试创建切片 CreateChunk 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err == nil {

	}
	//测试创建切片 CreateChunk 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err == nil {

	}
	//测试创建切片 CreateChunk 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err == nil {

	}
	//还原设置
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = clientT
	// 创建切片
	chunkID, err := client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create chunk failed: %v", err)
	}
	//还原设置
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = clientT

	//修改切片 ModifyChunk 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err == nil {

	}
	//修改切片 ModifyChunk 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err == nil {

	}
	//修改切片 ModifyChunk 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err == nil {

	}
	//修改切片 ModifyChunk 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err == nil {

	}
	//修改切片 ModifyChunk 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err == nil {

	}

	//还原设置
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = clientT

	//获取切片详情 DescribeChunk 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.DescribeChunk(chunkID)
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.DescribeChunk(chunkID)
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.DescribeChunk(chunkID)
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.DescribeChunk(chunkID)
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.DescribeChunk(chunkID)
	if err == nil {

	}

	//还原设置
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = clientT

	//获取切片详情 DescribeChunk 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	_, err = client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	_, err = client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	_, err = client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	_, err = client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err == nil {

	}
	//获取切片详情 DescribeChunk 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	_, err = client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err == nil {

	}

	time.Sleep(10 * time.Second)

	//还原设置
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = clientT

	//删除切片 DeleteChunk 测试1 ServiceURLV2 错误
	client.sdkConfig.GatewayURLV2 = "://invalid-url"
	err = client.DeleteChunk(chunkID)
	if err == nil {

	}
	//删除切片 DeleteChunk 测试2 Do 错误
	client.sdkConfig.GatewayURLV2 = "http://192.0.2.1"
	err = client.DeleteChunk(chunkID)
	if err == nil {

	}
	//删除切片 DeleteChunk 测试3  错误的 HTTP 响应
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &MockHTTPClient{}
	err = client.DeleteChunk(chunkID)
	if err == nil {

	}
	//删除切片 DeleteChunk 测试 4: 模拟读取 body 时发生错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &FaultyHTTPClient{}
	err = client.DeleteChunk(chunkID)
	if err == nil {

	}
	//删除切片 DeleteChunk 测试 5: json.Unmarshal错误
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = &InvalidJSONHTTPClient{}
	err = client.DeleteChunk(chunkID)
	if err == nil {

	}

	//还原设置
	client.sdkConfig.GatewayURLV2 = GatewayURL
	client.client = clientT
	// 删除切片
	err = client.DeleteChunk(chunkID)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("delete chunk failed: %v", err)
	}
}
func TestAddDocument(t *testing.T) {
	t.Parallel() // 并发运行
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	// 定义日志函数
	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	knowledgeBaseID := os.Getenv(DatasetIDV3)
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new Knowledge base instance failed")
	}

	documentsRes, err := client.GetDocumentList(GetDocumentListRequest{
		KnowledgeBaseID: knowledgeBaseID,
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("get document list failed: %v", err)
	}
	log("Documents retrieved: %+v", documentsRes)

	fileID, err := client.UploadFile("./files/test.pdf")
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upload file failed: %v", err)
	}
	log("File uploaded with ID: %s", fileID)

	createDocumentRes, err := client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create document failed: %v", err)
	}
	log("Document created: %+v", createDocumentRes)
	//正常测试部分
	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      createDocumentRes.DocumentsIDS[0]})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("delete document failed: %v", err)
	}
	log("Document deleted with ID: %s", createDocumentRes.DocumentsIDS[0])

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestCreateKnowledgeBase(t *testing.T) {
	t.Parallel() // 并发运行
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")

	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new Knowledge base instance failed")
	}

	// 创建知识库
	createKnowledgeBaseRes, err := client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create knowledge base failed: %v", err)
	}
	knowledgeBaseID := createKnowledgeBaseRes.ID
	log("Knowledge base created with ID: %s", knowledgeBaseID)

	// 获取知识库详情
	getKnowledgeBaseRes, err := client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("get knowledge base failed: %v", err)
	}
	log("Knowledge base details: %+v", getKnowledgeBaseRes)

	// 获取知识库列表
	knowledgeBaseListRes, err := client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("get knowledge base list failed: %v", err)
	}
	log("Knowledge base list: %+v", knowledgeBaseListRes)

	// 导入知识库
	err = client.CreateDocuments(CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type:     "web",
			Urls:     []string{"https://baijiahao.baidu.com/s?id=1802527379394162441"},
			UrlDepth: 1,
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create documents failed: %v", err)
	}
	log("Documents imported to knowledge base")

	// 上传知识库文档
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("upload documents failed: %v", err)
	}
	log("Documents uploaded to knowledge base")

	// 修改知识库
	name := "test-go"
	description := "22"
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("modify knowledge base failed: %v", err)
	}
	log("Knowledge base modified with new name: %s", name)

	// 删除知识库
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("delete knowledge base failed: %v", err)
	}
	log("Knowledge base deleted with ID: %s", knowledgeBaseID)

	// 测试通过，打印文件名和测试函数名
	t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		fmt.Println(logBuffer.String())
	}
}

func TestChunk(t *testing.T) {
	t.Parallel() // 并发运行
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")

	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	documentID := os.Getenv(DocumentIDV3)
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("new Knowledge base instance failed")
	}
	// 创建切片
	chunkID, err := client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("create chunk failed: %v", err)
	}
	log("Chunk created with ID: %s", chunkID)

	// 修改切片
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("modify chunk failed: %v", err)
	}
	log("Chunk modified with new content")

	// 获取切片详情
	describeChunkRes, err := client.DescribeChunk(chunkID)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("describe chunk failed: %v", err)
	}
	log("Chunk details: %+v", describeChunkRes)

	// 获取切片列表
	describeChunksRes, err := client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("describe chunks failed: %v", err)
	}
	log("Chunks described: %+v", describeChunksRes)

	time.Sleep(10 * time.Second)

	// 删除切片
	err = client.DeleteChunk(chunkID)
	if err != nil {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		t.Fatalf("delete chunk failed: %v", err)
	}
	log("Chunk deleted with ID: %s", chunkID)

	// 如果测试失败，则输出缓冲区中的日志
	if t.Failed() {
		t.Logf("%s========== FAIL:  %s ==========%s", "\033[31m", t.Name(), "\033[0m")
		fmt.Println(logBuffer.String())
	} else {  // else 紧跟在右大括号后面
		// 测试通过，打印文件名和测试函数名
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}