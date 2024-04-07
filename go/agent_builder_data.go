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

	"github.com/baidubce/appbuilder/internal/parser"
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
	Detail      interface{}
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
	Text  interface{} `json:"text"`
	Image string      `json:"image"`
	Audio string      `json:"audio"`
	Video string      `json:"video"`
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

func (t *AgentBuilderAnswer) transform(inp *AgentBuilderRawResponse) {
	t.Answer = inp.Answer
	for _, c := range inp.Content {
		ev := Event{Code: c.EventCode,
			Message:     c.EventMessage,
			Status:      c.EventStatus,
			EventType:   c.EventType,
			ContentType: c.ContentType,
			Detail:      c.Outputs}
		tp, ok := TypeToStruct[ev.ContentType]
		if !ok {
			ev.Detail = c.Outputs
		} else {
			v := reflect.New(tp)
			_ = json.Unmarshal(c.Outputs, v.Interface())
			ev.Detail = v.Elem().Interface()
		}
		t.Events = append(t.Events, ev)
	}
}

// AgentBuilderIterator  定义AgentBuilder流式/非流式统一的输出接口
// 迭代器初始状态可迭代,如果error返回不为空则代表迭代结束，对应如下两种情况：
// 1. 如果error为eoi，则代表迭代正常结束
// 2. 如果error不为空且不为eoi，则代表迭代异常
type AgentBuilderIterator interface {
	Next() (*AgentBuilderAnswer, error)
}

type AgentBuilderStreamIterator struct {
	body      io.ReadCloser
	p         *parser.Parser
	eof       bool
	closed    bool
	requestID string
}

func (t *AgentBuilderStreamIterator) Next() (*AgentBuilderAnswer, error) {
	for {
		if t.eof {
			return nil, eoi
		}
		event, err := readNext(t.p)
		if err != nil && !errors.Is(err, io.EOF) {
			return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
		}
		var data string
		if errors.Is(err, io.EOF) {
			t.eof = true
			data = event.Data
		} else {
			data = event.Data
		}
		if len(data) == 0 {
			continue
		}
		var resp AgentBuilderRawResponse
		if err := json.Unmarshal([]byte(event.Data), &resp); err != nil {
			return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
		}
		answer := &AgentBuilderAnswer{}
		answer.transform(&resp)
		return answer, nil
	}
}

type AgentBuilderOnceIterator struct {
	body      io.ReadCloser
	eoi       bool
	requestID string
}

func (t *AgentBuilderOnceIterator) Next() (*AgentBuilderAnswer, error) {
	if t.eoi {
		return nil, eoi
	}
	data, err := io.ReadAll(t.body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	defer t.body.Close()
	var resp AgentBuilderRawResponse
	if err := json.Unmarshal(data, &resp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	t.eoi = true
	answer := &AgentBuilderAnswer{}
	answer.transform(&resp)
	return answer, nil
}
