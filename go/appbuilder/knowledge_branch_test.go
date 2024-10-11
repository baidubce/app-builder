// knowledge_base_test.go
// Copyright (c) 2024 Baidu, Inc.
// All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");

package appbuilder

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"testing"
	"time"
)

// MockHTTPClient is a mock implementation of the HTTPClient interface.
type MockHTTPClient struct {
	Response *http.Response
	Err      error
}

func (m *MockHTTPClient) Do(req *http.Request) (*http.Response, error) {
	return m.Response, m.Err
}

// FaultyReader simulates an error when reading the response body.
type FaultyReader struct{}

func (f *FaultyReader) Read(p []byte) (n int, err error) {
	return 0, fmt.Errorf("simulated read error")
}

func (f *FaultyReader) Close() error {
	return nil
}

func TestAddDocument2(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

	// Define logging function
	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	knowledgeBaseID := os.Getenv(DatasetIDV3)
	if knowledgeBaseID == "" {
		knowledgeBaseID = "valid-knowledge-base-id"
	}
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed: %v", err)
	}

	// Test cases for GetDocumentList
	t.Run("GetDocumentList_Success", func(t *testing.T) {
		documentsRes, err := client.GetDocumentList(GetDocumentListRequest{
			KnowledgeBaseID: knowledgeBaseID,
		})
		if err != nil {
			t.Fatalf("get document list failed: %v", err)
		}
		log("Documents retrieved: %+v", documentsRes)
	})

	t.Run("GetDocumentList_InvalidID", func(t *testing.T) {
		invalidKnowledgeBaseID := "invalid-id"
		_, err := client.GetDocumentList(GetDocumentListRequest{
			KnowledgeBaseID: invalidKnowledgeBaseID,
		})
		if err == nil {
			t.Fatalf("expected error for invalid knowledge base ID")
		}
		log("Expected error for invalid knowledge base ID: %v", err)
	})

	// Upload a file
	fileID, err := client.UploadFile("./files/test.pdf")
	if err != nil {
		t.Fatalf("upload file failed: %v", err)
	}
	log("File uploaded with ID: %s", fileID)

	// Test cases for CreateDocument
	t.Run("CreateDocument_InvalidKnowledgeBaseID", func(t *testing.T) {
		_, err := client.CreateDocument(CreateDocumentRequest{
			KnowledgeBaseID: "invalid-id",
			ContentType:     ContentTypeRawText,
			FileIDS:         []string{fileID},
		})
		if err == nil {
			t.Fatalf("expected error when creating document with invalid knowledge base ID")
		}
		log("Expected error when creating document with invalid knowledge base ID: %v", err)
	})

	t.Run("CreateDocument_Success", func(t *testing.T) {
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
		log("Document created: %+v", createDocumentRes)

		// Delete the document
		err = client.DeleteDocument(DeleteDocumentRequest{
			KnowledgeBaseID: knowledgeBaseID,
			DocumentID:      createDocumentRes.DocumentsIDS[0],
		})
		if err != nil {
			t.Fatalf("delete document failed: %v", err)
		}
		log("Document deleted with ID: %s", createDocumentRes.DocumentsIDS[0])
	})

	t.Run("DeleteDocument_InvalidDocumentID", func(t *testing.T) {
		err := client.DeleteDocument(DeleteDocumentRequest{
			KnowledgeBaseID: knowledgeBaseID,
			DocumentID:      "invalid-document-id",
		})
		if err == nil {
			t.Fatalf("expected error when deleting document with invalid ID")
		}
		log("Expected error when deleting document with invalid ID: %v", err)
	})

	// Simulate HTTP client error
	t.Run("CreateDocument_HTTPClientError", func(t *testing.T) {
		mockClient := &MockHTTPClient{
			Response: nil,
			Err:      fmt.Errorf("simulated HTTP client error"),
		}
		config.HTTPClient = mockClient
		client, _ := NewKnowledgeBase(config)

		_, err := client.CreateDocument(CreateDocumentRequest{
			KnowledgeBaseID: knowledgeBaseID,
			ContentType:     ContentTypeRawText,
			FileIDS:         []string{fileID},
		})
		if err == nil || !strings.Contains(err.Error(), "simulated HTTP client error") {
			t.Fatalf("expected simulated HTTP client error, got: %v", err)
		}
		log("Expected simulated HTTP client error: %v", err)
	})

	// Simulate non-200 HTTP response
	t.Run("CreateDocument_HTTPNonOKStatus", func(t *testing.T) {
		mockResp := &http.Response{
			StatusCode: http.StatusBadRequest,
			Header:     make(http.Header),
			Body:       io.NopCloser(bytes.NewBufferString(`{"code": "InvalidRequest", "message": "Invalid request"}`)),
		}
		mockResp.Header.Set("X-Appbuilder-Request-Id", "test-request-id")

		mockClient := &MockHTTPClient{
			Response: mockResp,
			Err:      nil,
		}
		config.HTTPClient = mockClient
		client, _ := NewKnowledgeBase(config)

		_, err := client.CreateDocument(CreateDocumentRequest{
			KnowledgeBaseID: knowledgeBaseID,
			ContentType:     ContentTypeRawText,
			FileIDS:         []string{fileID},
		})
		if err == nil || !strings.Contains(err.Error(), "http status code is 400") {
			t.Fatalf("expected HTTP 400 error, got: %v", err)
		}
		log("Expected HTTP 400 error: %v", err)
	})

	// Simulate error in reading response body
	t.Run("CreateDocument_ResponseBodyReadError", func(t *testing.T) {
		mockResp := &http.Response{
			StatusCode: http.StatusOK,
			Header:     make(http.Header),
			Body:       &FaultyReader{},
		}
		mockResp.Header.Set("X-Appbuilder-Request-Id", "test-request-id")

		mockClient := &MockHTTPClient{
			Response: mockResp,
			Err:      nil,
		}
		config.HTTPClient = mockClient
		client, _ := NewKnowledgeBase(config)

		_, err := client.CreateDocument(CreateDocumentRequest{
			KnowledgeBaseID: knowledgeBaseID,
			ContentType:     ContentTypeRawText,
			FileIDS:         []string{fileID},
		})
		if err == nil || !strings.Contains(err.Error(), "simulated read error") {
			t.Fatalf("expected error in reading response body, got: %v", err)
		}
		log("Expected error in reading response body: %v", err)
	})

	// If test failed, output log buffer
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else {
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestCreateKnowledgeBase2(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")

	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}

	// Test cases for CreateKnowledgeBase
	t.Run("CreateKnowledgeBase_Success", func(t *testing.T) {
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
		log("Knowledge base created with ID: %s", knowledgeBaseID)

		// Get knowledge base detail
		getKnowledgeBaseRes, err := client.GetKnowledgeBaseDetail(knowledgeBaseID)
		if err != nil {
			t.Fatalf("get knowledge base failed: %v", err)
		}
		log("Knowledge base details: %+v", getKnowledgeBaseRes)

		// Modify knowledge base with invalid data
		err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
			ID:          knowledgeBaseID,
			Name:        nil,
			Description: nil,
		})
		if err != nil {
			t.Fatalf("modify knowledge base failed with nil values: %v", err)
		}
		log("Knowledge base modified with nil values")

		// Delete knowledge base
		err = client.DeleteKnowledgeBase(knowledgeBaseID)
		if err != nil {
			t.Fatalf("delete knowledge base failed: %v", err)
		}
		log("Knowledge base deleted with ID: %s", knowledgeBaseID)
	})

	t.Run("CreateKnowledgeBase_InvalidConfig", func(t *testing.T) {
		_, err := client.CreateKnowledgeBase(KnowledgeBaseDetail{
			Name:        "",
			Description: "",
			Config:      nil,
		})
		if err == nil {
			t.Fatalf("expected error when creating knowledge base with invalid config")
		}
		log("Expected error when creating knowledge base with invalid config: %v", err)
	})

	// If test failed, output log buffer
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else {
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}

func TestChunk2(t *testing.T) {
	var logBuffer bytes.Buffer

	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")

	log := func(format string, args ...interface{}) {
		fmt.Fprintf(&logBuffer, format+"\n", args...)
	}

	documentID := os.Getenv(DocumentIDV3)
	if documentID == "" {
		documentID = "valid-document-id"
	}
	config, err := NewSDKConfig("", os.Getenv(SecretKeyV3))
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}

	// Test cases for CreateChunk
	t.Run("CreateChunk_Success", func(t *testing.T) {
		chunkID, err := client.CreateChunk(CreateChunkRequest{
			DocumentID: documentID,
			Content:    "test content",
		})
		if err != nil {
			t.Fatalf("create chunk failed: %v", err)
		}
		log("Chunk created with ID: %s", chunkID)

		// Modify chunk
		err = client.ModifyChunk(ModifyChunkRequest{
			ChunkID: chunkID,
			Content: "updated test content",
			Enable:  true,
		})
		if err != nil {
			t.Fatalf("modify chunk failed: %v", err)
		}
		log("Chunk modified with new content")

		// Describe chunk
		describeChunkRes, err := client.DescribeChunk(chunkID)
		if err != nil {
			t.Fatalf("describe chunk failed: %v", err)
		}
		log("Chunk details: %+v", describeChunkRes)

		// Describe chunks
		describeChunksRes, err := client.DescribeChunks(DescribeChunksRequest{
			DocumnetID: documentID,
			MaxKeys:    10,
		})
		if err != nil {
			t.Fatalf("describe chunks failed: %v", err)
		}
		log("Chunks described: %+v", describeChunksRes)

		time.Sleep(10 * time.Second)

		// Delete chunk
		err = client.DeleteChunk(chunkID)
		if err != nil {
			t.Fatalf("delete chunk failed: %v", err)
		}
		log("Chunk deleted with ID: %s", chunkID)
	})

	t.Run("CreateChunk_InvalidDocumentID", func(t *testing.T) {
		_, err := client.CreateChunk(CreateChunkRequest{
			DocumentID: "invalid-document-id",
			Content:    "test content",
		})
		if err == nil {
			t.Fatalf("expected error when creating chunk with invalid document ID")
		}
		log("Expected error when creating chunk with invalid document ID: %v", err)
	})

	// If test failed, output log buffer
	if t.Failed() {
		fmt.Println(logBuffer.String())
	} else {
		t.Logf("%s========== OK:  %s ==========%s", "\033[32m", t.Name(), "\033[0m")
	}
}