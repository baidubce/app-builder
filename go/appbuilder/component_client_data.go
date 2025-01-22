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
	"encoding/json"
	"fmt"
	"io"
	"strings"
)

const (
	SysOriginQuery    = "_sys_origin_query"
	SysFileUrls       = "_sys_file_urls"
	SysConversationID = "_sys_conversation_id"
	SysEndUserID      = "_sys_end_user_id"
	SysChatHistory    = "_sys_chat_history"
)

type ComponentRunRequest struct {
	Stream     bool           `json:"stream"`
	Parameters map[string]any `json:"parameters"`
}

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ComponentRunResponse struct {
	RequestID      string    `json:"request_id"`
	Code           string    `json:"code"`
	Message        string    `json:"message"`
	ConversationID string    `json:"conversation_id"`
	MessageID      string    `json:"message_id"`
	TraceID        string    `json:"trace_id"`
	UserID         string    `json:"user_id"`
	EndUserID      string    `json:"end_user_id"`
	Status         string    `json:"status"` // 新增的字段
	Role           string    `json:"role"`
	Content        []Content `json:"content"`
}

type Content struct {
	Name         string         `json:"name"`
	VisibleScope string         `json:"visible_scope"`
	RawData      map[string]any `json:"raw_data"`
	Usage        map[string]any `json:"usage"`
	Metrics      map[string]any `json:"metrics"`
	Type         string         `json:"type"`
	Text         map[string]any `json:"text"`
	Event        ComponentEvent `json:"event"`
}

type ComponentEvent struct {
	ID           string `json:"id"`
	Status       string `json:"status"`
	Name         string `json:"name"`
	CreatedTime  string `json:"created_time"`
	ErrorCode    string `json:"error_code"`
	ErrorMessage string `json:"error_message"`
}

type Text struct {
	Info string `json:"info"`
}

type Code struct {
	Code string `json:"code"`
}

type Files struct {
	Filename string `json:"filename"`
	Url      string `json:"url"`
}

type Urls struct {
	Url string `json:"url"`
}

type OralText struct {
	Info string `json:"info"`
}

type References struct {
	Type    string         `json:"type"`
	Source  string         `json:"source"`
	DocID   string         `json:"doc_id"`
	Title   string         `json:"title"`
	Content string         `json:"content"`
	Extra   map[string]any `json:"extra"`
}

type Image struct {
	Filename string `json:"filename"`
	Url      string `json:"url"`
	Byte     []byte `json:"byte"`
}

type Chart struct {
	Type string `json:"type"`
	Data string `json:"data"`
}

type Audio struct {
	Filename string `json:"filename"`
	Url      string `json:"url"`
	Byte     []byte `json:"byte"`
}

type PlanStep struct {
	Name      string         `json:"name"`
	Arguments map[string]any `json:"arguments"`
	Thought   string         `json:"thought"`
}

type Plan struct {
	Detail string     `json:"detail"`
	Steps  []PlanStep `json:"steps"`
}

type FunctionCall struct {
	Thought   string         `json:"thought"`
	Name      string         `json:"name"`
	Arguments map[string]any `json:"arguments"`
}

type Json struct {
	Data string `json:"data"`
}

type ComponentClientIterator interface {
	// Next 获取处理结果，如果返回error不为空，迭代器自动失效，不允许再调用此方法
	Next() (*ComponentRunResponseData, error)
}

type ComponentClientStreamIterator struct {
	requestID string
	r         *sseReader
	body      io.ReadCloser
}

func (t *ComponentClientStreamIterator) Next() (*ComponentRunResponseData, error) {
	data, err := t.r.ReadMessageLine()
	if err != nil && !(err == io.EOF) {
		t.body.Close()
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	if err != nil && err == io.EOF {
		t.body.Close()
		return nil, err
	}
	if strings.HasPrefix(string(data), "data:") {
		var resp ComponentRunResponse
		if err := json.Unmarshal(data[5:], &resp); err != nil {
			t.body.Close()
			return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
		}
		return &resp.Data, nil
	}
	// 非SSE格式关闭连接，并返回数据
	t.body.Close()
	return nil, fmt.Errorf("requestID=%s, body=%s", t.requestID, string(data))
}

// ComponentClientOnceIterator 非流式返回时对应的迭代器，只可迭代一次
type ComponentClientOnceIterator struct {
	body      io.ReadCloser
	requestID string
}

func (t *ComponentClientOnceIterator) Next() (*ComponentRunResponseData, error) {
	data, err := io.ReadAll(t.body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	defer t.body.Close()
	var resp ComponentRunResponse
	if err := json.Unmarshal(data, &resp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	return &resp.Data, nil
}
