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
	ClientToken       string             `json:"client_token,omitempty"`
}

type DeleteDocumentRequest struct {
	KnowledgeBaseID string `json:"knowledge_base_id"`
	DocumentID      string `json:"document_id"`
	ClientToken     string `json:"client_token,omitempty"`
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

type KnowlegeBaseConfig struct {
	Index KnowledgeBaseConfigIndex `json:"index"`
}

type KnowledgeBaseConfigIndex struct {
	Type     string `json:"type"`
	EsUrl    string `json:"esUrl"`
	Username string `json:"username"`
	Password string `json:"password"`
}

type KnowledgeBaseDetail struct {
	ID          string              `json:"id,omitempty"`
	Name        string              `json:"name,omitempty"`
	Description string              `json:"description,omitempty"`
	Config      *KnowlegeBaseConfig `json:"config,omitempty"`
	ClientToken string              `json:"client_token,omitempty"`
}

type ModifyKnowlegeBaseRequest struct {
	ID          string  `json:"id"`
	Name        *string `json:"name,omitempty"`
	Description *string `json:"description,omitempty"`
	ClientToken string  `json:"client_token,omitempty"`
}

type DeleteKnowlegeBaseRequest struct {
	ID          string `json:"id"`
	ClientToken string `json:"client_token,omitempty"`
}

type GetKnowledgeBaseListRequest struct {
	Marker  string `json:"marker,omitempty"`
	Keyword string `json:"keyword,omitempty"`
	MaxKeys int    `json:"maxKeys,omitempty"`
}

type GetKnowledgeBaseListResponse struct {
	RequestID   string                `json:"requestId"`
	Data        []KnowledgeBaseDetail `json:"data"`
	Marker      string                `json:"marker"`
	IsTruncated bool                  `json:"isTruncated"`
	NextMarker  string                `json:"nextMarker"`
	MaxKeys     int                   `json:"maxKeys"`
}

type DocumentsSource struct {
	Type     string   `json:"type"`
	Urls     []string `json:"urls,omitempty"`
	UrlDepth int      `json:"url_depth,omitempty"`
}

type DocumentsProcessOptionParser struct {
	Choices []string `json:"choices"`
}

type DocumentsProcessOptionChunkerSeparator struct {
	Separators   []string `json:"separators"`
	TargetLength int64    `json:"targetLength"`
	OverlapRate  float64  `json:"overlapRate"`
}

type DocumentsProcessOptionChunkerPattern struct {
	MarkPosition string  `json:"markPosition"`
	Regex        string  `json:"regex"`
	TargetLength int64   `json:"targetLength"`
	OverlapRate  float64 `json:"overlapRate"`
}

type DocumentsProcessOptionChunker struct {
	Choices     []string                                `json:"choices"`
	PrependInfo []string                                `json:"prependInfo"`
	Separator   *DocumentsProcessOptionChunkerSeparator `json:"separator,omitempty"`
	Pattern     *DocumentsProcessOptionChunkerPattern   `json:"pattern,omitempty"`
}

type DocumentsProcessOptionKnowledgeAugmentation struct {
	Choices []string `json:"choices"`
}

type DocumentsProcessOption struct {
	Template              string                                       `json:"template"`
	Parser                *DocumentsProcessOptionParser                `json:"parser,omitempty"`
	Chunker               *DocumentsProcessOptionChunker               `json:"chunker,omitempty"`
	KnowledgeAugmentation *DocumentsProcessOptionKnowledgeAugmentation `json:"knowledgeAugmentation,omitempty"`
}

type CreateDocumentsRequest struct {
	ID            string                  `json:"id"`
	ContentFormat string                  `json:"contentFormat"`
	Source        DocumentsSource         `json:"source"`
	ProcessOption *DocumentsProcessOption `json:"processOption,omitempty"`
	ClientToken   string                  `json:"client_token,omitempty"`
}

type CreateChunkRequest struct {
	DocumentID  string `json:"documentId"`
	Content     string `json:"content"`
	ClientToken string `json:"client_token,omitempty"`
}

type CreateChunkResponse struct {
	ID string `json:"id"`
}

type ModifyChunkRequest struct {
	ChunkID     string `json:"chunkId"`
	Content     string `json:"content"`
	Enable      bool   `json:"enable"`
	ClientToken string `json:"client_token,omitempty"`
}

type DeleteChunkRequest struct {
	ChunkID     string `json:"chunkId"`
	ClientToken string `json:"client_token,omitempty"`
}

type DescribeChunkRequest struct {
	ChunkID string `json:"chunkId"`
}

type DescribeChunkResponse struct {
	ID              string   `json:"id"`
	Type            string   `json:"type"`
	KnowledgeBaseID string   `json:"knowledgeBaseId"`
	DocumentID      string   `json:"documentId"`
	Content         string   `json:"content"`
	WordCount       int64    `json:"wordCount"`
	TokenCount      int64    `json:"tokenCount"`
	Enabled         bool     `json:"enabled"`
	Status          string   `json:"status"`
	StatusMessage   string   `json:"statusMessage"`
	ImageUrls       []string `json:"imageUrls"`
	CreatedAt       int64    `json:"createTime"`
	UpdatedAt       int64    `json:"updateTime"`
}

type DescribeChunksRequest struct {
	DocumnetID string `json:"documentId"`
	Marker     string `json:"marker,omitempty"`
	MaxKeys    int    `json:"maxKeys,omitempty"`
	Type       string `json:"type,omitempty"`
}

type DescribeChunksResponse struct {
	Data        []DescribeChunkResponse `json:"data"`
	Marker      string                  `json:"marker"`
	IsTruncated bool                    `json:"isTruncated"`
	NextMarker  string                  `json:"nextMarker"`
	MaxKeys     int                     `json:"maxKeys"`
}
