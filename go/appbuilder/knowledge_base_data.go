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

const (
	ContentTypeRawText = "raw_text"
	ContentTypeQA      = "qa"
)

type CreateDocumentRequest struct {
	KnowledgeBaseID   string             `json:"knowledge_base_id"`
	ContentType       string             `json:"content_type"`
	IsEnhanced        bool               `json:"is_enhanced"`
	FileIDS           []string           `json:"file_ids,omitempty"`
	CustomProcessRule *CustomProcessRule `json:"custom_process_rule,omitempty"`
}

type DeleteDocumentRequest struct {
	KnowledgeBaseID string `json:"knowledge_base_id"`
	DocumentID      string `json:"document_id"`
}

type GetDocumentListRequest struct {
	KnowledgeBaseID string `json:"knowledge_base_id"`
	Limit           int    `json:"limit,omitempty"`
	After           string `json:"after,omitempty"`
	Before          string `json:"before,omitempty"`
}

type CustomProcessRule struct {
	Separators   []string `json:"separators"`
	TargetLength int64    `json:"target_length"`
	OverlapRate  float64  `json:"overlap_rate"`
}

type CreateDocumentResponse struct {
	RequestID       string   `json:"request_id"`
	KnowledgeBaseID string   `json:"knowledge_base_id"`
	DocumentsIDS    []string `json:"document_ids"`
	Code            string   `json:"code"`
	Message         string   `json:"message"`
}

type GetDocumentListResponse struct {
	RequestID string     `json:"request_id"`
	Data      []Document `json:"data"`
	Code      string     `json:"code"`
	Message   string     `json:"message"`
}

type Document struct {
	ID        string       `json:"id"`
	Name      string       `json:"name"`
	CreatedAt any          `json:"created_at"`
	WordCount int64        `json:"word_count"`
	Enabled   bool         `json:"enabled"`
	Meta      DocumentMeta `json:"meta"`
}

type DocumentMeta struct {
	Source string `json:"source"`
	FileID string `json:"file_id"`
}

type UploadFileResponse struct {
	RequestID string `json:"request_id"`
	FileID    string `json:"id"`
	FileName  string `json:"name"`
	Code      string `json:"code"`
	Message   string `json:"message"`
}
