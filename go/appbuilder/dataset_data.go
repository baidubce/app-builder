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

type DatasetResponse struct {
	Code    int            `json:"code"`
	Message string         `json:"message"`
	Result  map[string]any `json:"result"`
}

type DatasetBindResponse struct {
	Code    int               `json:"code"`
	Message string            `json:"message"`
	Result  DatasetBindResult `json:"result"`
}

type DatasetBindResult struct {
	DocumentIDs []string `json:"document_ids"`
}

type ListDocumentResponse struct {
	Code    int                        `json:"code"`
	Message string                     `json:"message"`
	Result  ListDocumentResponseResult `json:"result"`
}

type ListDocumentResponseResult struct {
	HasMore bool       `json:"has_more"`
	Limit   int        `json:"limit"`
	Total   int        `json:"total"`
	Page    int        `json:"page"`
	Data    []FileInfo `json:"data"`
}

type FileInfo struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}
