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
	"time"
)

func TestAddDocument(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")
	knowledgeBaseID := "4b2357ff-b7d5-4573-9187-ee29af2f8373"
	config, err := NewSDKConfig("", "bce-v3/ALTAK-DKaql4wY9ojwp2uMe8IEj/7ae1190aff0684153de365381d9b06beab3064c5")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}

	documentsRes, err := client.GetDocumentList(GetDocumentListRequest{
		KnowledgeBaseID: knowledgeBaseID,
	})
	if err != nil {
		t.Fatalf("create document failed: %v", err)
	}
	fmt.Println(documentsRes)
	fileID, err := client.UploadFile("./files/test.pdf")
	if err != nil {
		t.Fatalf("upload file failed: %v", err)
	}
	fmt.Println(fileID)
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
		t.Fatalf("create document failed: %v", err)
	}
	fmt.Println(createDocumentRes)

	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      createDocumentRes.DocumentsIDS[0]})
	if err != nil {
		t.Fatalf("delete document failed: %v", err)
	}
}

func TestCreateKnowledgeBase(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")
	config, err := NewSDKConfig("", "bce-v3/ALTAK-DKaql4wY9ojwp2uMe8IEj/7ae1190aff0684153de365381d9b06beab3064c5")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
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
		t.Fatalf("create knowledge base failed: %v", err)
	}
	knowledgeBaseID := createKnowledgeBaseRes.ID
	fmt.Println(knowledgeBaseID)

	// 获取知识库详情
	getKnowledgeBaseRes, err := client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err != nil {
		t.Fatalf("get knowledge base failed: %v", err)
	}
	fmt.Println(getKnowledgeBaseRes)

	// 获取知识库列表
	knowledgeBaseListRes, err := client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err != nil {
		t.Fatalf("get knowledge base list failed: %v", err)
	}
	fmt.Println(knowledgeBaseListRes)

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
		t.Fatalf("create documents failed: %v", err)
	}

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
		t.Fatalf("upload documents failed: %v", err)
	}

	// 修改知识库
	name := "test-go"
	description := "22"
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err != nil {
		t.Fatalf("modify knowledge base failed: %v", err)
	}

	// 删除知识库
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err != nil {
		t.Fatalf("delete knowledge base failed: %v", err)
	}
}

func TestChunk(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")
	documentID := "120619f2-1b85-4e09-a36d-fc682168d09c"

	config, err := NewSDKConfig("", "bce-v3/ALTAK-DKaql4wY9ojwp2uMe8IEj/7ae1190aff0684153de365381d9b06beab3064c5")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}
	// 创建切片
	chunkID, err := client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err != nil {
		t.Fatalf("create chunk failed: %v", err)
	}
	fmt.Println(chunkID)

	// 修改切片
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err != nil {
		t.Fatalf("modify chunk failed: %v", err)
	}

	// 获取切片详情
	describeChunkRes, err := client.DescribeChunk(chunkID)
	if err != nil {
		t.Fatalf("describe chunk failed: %v", err)
	}
	fmt.Println(describeChunkRes)

	// 获取切片列表
	describeChunksRes, err := client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err != nil {
		t.Fatalf("describe chunks failed: %v", err)
	}
	fmt.Println(describeChunksRes)
	time.Sleep(10 * time.Second)
	// 删除切片
	err = client.DeleteChunk(chunkID)
	if err != nil {
		t.Fatalf("delete chunk failed: %v", err)
	}
}
