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

type QueryType string

const (
    Fulltext QueryType = "fulltext"
    Semantic QueryType = "semantic"
    Hybrid   QueryType = "hybrid"
)

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

type CreateDocumentsResponse struct {
	RequestID   string   `json:"requestId"`
	DocumentIDS []string `json:"documentIds"`
}

type UploadDocumentsResponse struct {
	RequestID  string `json:"requestId"`
	DocumentID string `json:"documentId"`
}

type CreateChunkRequest struct {
	KnowledgeBaseID string `json:"knowledgeBaseId"`
	DocumentID      string `json:"documentId"`
	Content         string `json:"content"`
	ClientToken     string `json:"client_token,omitempty"`
}

type CreateChunkResponse struct {
	ID string `json:"id"`
}

type ModifyChunkRequest struct {
	KnowledgeBaseID string `json:"knowledgeBaseId"`
	ChunkID         string `json:"chunkId"`
	Content         string `json:"content"`
	Enable          bool   `json:"enable"`
	ClientToken     string `json:"client_token,omitempty"`
}

type DeleteChunkRequest struct {
	KnowledgeBaseID string `json:"knowledgeBaseId"`
	ChunkID         string `json:"chunkId"`
	ClientToken     string `json:"client_token,omitempty"`
}

type DescribeChunkRequest struct {
	KnowledgeBaseID string `json:"knowledgeBaseId"`
	ChunkID         string `json:"chunkId"`
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
	KnowledgeBaseID string `json:"knowledgeBaseId"`
	DocumnetID      string `json:"documentId"`
	Marker          string `json:"marker,omitempty"`
	MaxKeys         int    `json:"maxKeys,omitempty"`
	Type            string `json:"type,omitempty"`
}

type DescribeChunksResponse struct {
	Data        []DescribeChunkResponse `json:"data"`
	Marker      string                  `json:"marker"`
	IsTruncated bool                    `json:"isTruncated"`
	NextMarker  string                  `json:"nextMarker"`
	MaxKeys     int                     `json:"maxKeys"`
}

type MetadataFilter struct {
	Operator string `json:"operator"`
	Field    string `json:"field,omitempty"`
	Value    any    `json:"value"`
}

type MetadataFilters struct {
	Filters   []MetadataFilter `json:"filters"`
	Condition string           `json:"condition"`
}

type PreRankingConfig struct {
	Bm25Weight   float64 `json:"bm25_weight"`
	VecWeight    float64 `json:"vec_weight"`
	Bm25B        float64 `json:"bm25_b"`
	Bm25K1       float64 `json:"bm25_k1"`
	Bm25MaxScore float64 `json:"bm25_max_score"`
}

type ElasticSearchRetrieveConfig struct {
	Name      string  `json:"name"`
	Type      string  `json:"type"`
	Threshold float64 `json:"threshold"`
	Top       int     `json:"top"`
}

type VectorDBRetrieveConfig struct {
	Name      string  `json:"name"`
	Type      string  `json:"type"`
	Threshold float64 `json:"threshold"`
	Top       int     `json:"top"`
}

type SmallToBigConfig struct {
	Name      string   `json:"name"`
	Type      string   `json:"type"`
}

type RankingConfig struct {
	Name      string   `json:"name"`
	Type      string   `json:"type"`
	Inputs    []string `json:"inputs"`
	ModelName string   `json:"model_name"`
	Top       int      `json:"top"`
}

type QueryPipelineConfig struct {
	ID       string `json:"id"`
	Pipeline []any  `json:"pipeline"`
}

type QueryKnowledgeBaseRequest struct {
	Query            		string              `json:"query"`
	KnowledgebaseIDs 		[]string            `json:"knowledgebase_ids"`
	Type             		*QueryType          `json:"type,omitempty"`
	Top              		int                 `json:"top,omitempty"`
	Skip             		int                 `json:"skip,omitempty"`
	rank_score_threshold 	*float64         	`json:"rank_score_threshold,omitempty"`
	MetadataFileters 		MetadataFilters     `json:"metadata_fileters,omitempty"`
	PipelineConfig   		QueryPipelineConfig `json:"pipeline_config,omitempty"`
}

type RowLine struct {
	Key            string `json:"key"`
	Index          int    `json:"index"`
	Value          string `json:"value"`
	EnableIndexing bool   `json:"enable_indexing"`
	EnableResponse bool   `json:"enable_response"`
}

type ChunkLocation struct {
	PageNum []int   `json:"paget_num"`
	Box     [][]int `json:"box"`
}

type Chunk struct {
	ChunkID         	string         `json:"chunk_id"`
	KnowledgebaseID 	string         `json:"knowledgebase_id"`
	DocumentID      	string         `json:"document_id"`
	DocumentName    	string         `json:"document_name"`
	Meta            	map[string]any `json:"meta"`
	Type            	string         `json:"type"`
	Content         	string         `json:"content"`
	CreateTime      	string         `json:"create_time"`
	UpdateTime      	string         `json:"update_time"`
	RetrievalScore  	float64        `json:"retrieval_score"`
	RankScore       	float64        `json:"rank_score"`
	Locations       	ChunkLocation  `json:"locations"`
	Children        	[]Chunk        `json:"children"`
	NeighbourChunks     []Chunk        `json:"neighbour_chunks"`
	OriginalChunkId 	string         `json:"original_chunk_id"`
	OriginalChunkOffset int        	   `json:"original_chunk_offset"`
}

type QueryKnowledgeBaseResponse struct {
	RequestId  string  `json:"requestId"`
	Code       string  `json:"code"`
	Message    string  `json:"message"`
	Chunks     []Chunk `json:"chunks"`
	TotalCount int     `json:"total_count"`
}
