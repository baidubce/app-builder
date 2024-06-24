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
	"errors"
	"fmt"
	"io"
	"reflect"
	"strings"
)

const (
	CodeContentType         = "code"
	TextContentType         = "text"
	ImageContentType        = "image"
	RAGContentType          = "rag"
	FunctionCallContentType = "function_call"
	AudioContentType        = "audio"
	VideoContentType        = "video"
	StatusContentType       = "status"
)

var TypeToStruct = map[string]reflect.Type{
	CodeContentType:         reflect.TypeOf(CodeDetail{}),
	TextContentType:         reflect.TypeOf(TextDetail{}),
	ImageContentType:        reflect.TypeOf(ImageDetail{}),
	RAGContentType:          reflect.TypeOf(RAGDetail{}),
	FunctionCallContentType: reflect.TypeOf(FunctionCallDetail{}),
	AudioContentType:        reflect.TypeOf(AudioDetail{}),
	VideoContentType:        reflect.TypeOf(VideoDetail{}),
	StatusContentType:       reflect.TypeOf(StatusDetail{}),
}

type AgentBuilderRawResponse struct {
	RequestID      string           `json:"request_id"`
	Date           string           `json:"date"`
	Answer         string           `json:"answer"`
	ConversationID string           `json:"conversation_id"`
	MessageID      string           `json:"message_id"`
	IsCompletion   bool             `json:"is_completion"`
	Content        []RawEventDetail `json:"content"`
}

type RawEventDetail struct {
	EventCode    int             `json:"event_code"`
	EventMessage string          `json:"event_message"`
	EventType    string          `json:"event_type"`
	EventID      string          `json:"event_id"`
	EventStatus  string          `json:"event_status"`
	ContentType  string          `json:"content_type"`
	Outputs      json.RawMessage `json:"outputs"`
	Usage        Usage           `json:"usage"`
}

type Usage struct {
	PromptTokens     int    `json:"prompt_tokens"`
	CompletionTokens int    `json:"completion_tokens"`
	TotalTokens      int    `json:"total_tokens"`
	Name             string `json:"name"`
}

type AgentBuilderAnswer struct {
	Answer string
	Events []Event
}

type Event struct {
	Code        int
	Message     string
	Status      string
	EventType   string
	ContentType string
	Usage       Usage
	Detail      any
}

type TextDetail struct {
	Text string `json:"text"`
}

type CodeDetail struct {
	Text  string   `json:"text"`
	Code  string   `json:"code"`
	Files []string `json:"files"`
}

type RAGDetail struct {
	Text       string      `json:"text"`
	References []Reference `json:"references"`
}

type Reference struct {
	ID           string `json:"id"`
	From         string `json:"from"`
	URL          string `json:"url"`
	Content      string `json:"content"`
	SegmentID    string `json:"segment_id"`
	DocumentID   string `json:"document_id"`
	DatasetID    string `json:"dataset_id"`
	DocumentName string `json:"document_name"`
}

type FunctionCallDetail struct {
	Text  any    `json:"text"`
	Image string `json:"image"`
	Audio string `json:"audio"`
	Video string `json:"video"`
}

type ImageDetail struct {
	Image string `json:"image"`
}

type AudioDetail struct {
	Audio string `json:"audio"`
}

type VideoDetail struct {
	Video string `json:"video"`
}

type StatusDetail struct{}

type DefaultDetail struct {
	URLS  []string `json:"urls"`
	Files []string `json:"files"`
	Image string   `json:"image"`
	Video string   `json:"video"`
	Audio string   `json:"audio"`
}

type AppBuilderClientRawResponse struct {
	RequestID      string           `json:"request_id"`
	Date           string           `json:"date"`
	Answer         string           `json:"answer"`
	ConversationID string           `json:"conversation_id"`
	MessageID      string           `json:"message_id"`
	IsCompletion   bool             `json:"is_completion"`
	Content        []RawEventDetail `json:"content"`
}

type GetAppListRequest struct {
	Limit  int    `json:"limit"`
	After  string `json:"after"`
	Before string `json:"before"`
}

type GetAppListResponse struct {
	RequestID string `json:"request_id"`
	Data      []App  `json:"data"`
	Code      string `json:"code"`
	Message   string `json:"message"`
}

type App struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
}

type AppBuilderClientAnswer struct {
	Answer string
	Events []Event
}

func (t *AppBuilderClientAnswer) transform(inp *AppBuilderClientRawResponse) {
	t.Answer = inp.Answer
	for _, c := range inp.Content {
		ev := Event{Code: c.EventCode,
			Message:     c.EventMessage,
			Status:      c.EventStatus,
			EventType:   c.EventType,
			ContentType: c.ContentType,
			Usage:       c.Usage,
			Detail:      c.Outputs}
		tp, ok := TypeToStruct[ev.ContentType]
		if !ok {
			tp = reflect.TypeOf(DefaultDetail{})
		}
		v := reflect.New(tp)
		_ = json.Unmarshal(c.Outputs, v.Interface())
		ev.Detail = v.Elem().Interface()
		t.Events = append(t.Events, ev)
	}
}

// AppBuilderClientIterator 定义AppBuilderClient流式/非流式迭代器接口
// 初始状态可迭代,如果返回error不为空则代表迭代结束，
// error为io.EOF，则代表迭代正常结束，其它则为异常结束
type AppBuilderClientIterator interface {
	// Next 获取处理结果，如果返回error不为空，迭代器自动失效，不允许再调用此方法
	Next() (*AppBuilderClientAnswer, error)
}

type AppBuilderClientStreamIterator struct {
	requestID string
	r         *sseReader
	body      io.ReadCloser
}

func (t *AppBuilderClientStreamIterator) Next() (*AppBuilderClientAnswer, error) {
	data, err := t.r.ReadMessageLine()
	if err != nil && !errors.Is(err, io.EOF) {
		t.body.Close()
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	if err != nil && errors.Is(err, io.EOF) {
		t.body.Close()
		return nil, err
	}
	if strings.HasPrefix(string(data), "data:") {
		var resp AppBuilderClientRawResponse
		if err := json.Unmarshal(data[5:], &resp); err != nil {
			t.body.Close()
			return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
		}
		answer := &AppBuilderClientAnswer{}
		answer.transform(&resp)
		return answer, nil
	}
	// 非SSE格式关闭连接，并返回数据
	t.body.Close()
	return nil, fmt.Errorf("requestID=%s, body=%s", t.requestID, string(data))
}

// AppBuilderClientOnceIterator 非流式返回时对应的迭代器，只可迭代一次
type AppBuilderClientOnceIterator struct {
	body      io.ReadCloser
	requestID string
}

func (t *AppBuilderClientOnceIterator) Next() (*AppBuilderClientAnswer, error) {
	data, err := io.ReadAll(t.body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	defer t.body.Close()
	var resp AppBuilderClientRawResponse
	if err := json.Unmarshal(data, &resp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	answer := &AppBuilderClientAnswer{}
	answer.transform(&resp)
	return answer, nil
}
