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
)

func TestAddDocument(t *testing.T) {
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