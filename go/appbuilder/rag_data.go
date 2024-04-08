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

	"github.com/baidubce/app-builder/go/appbuilder/internal/parser"
)

type RAGRunResponse struct {
	Code    int       `json:"code"`
	Message string    `json:"message"`
	Result  RAGResult `json:"result"`
}

type RAGResult struct {
	ConversationID string     `json:"conversation_id"`
	Answer         string     `json:"answer"`
	Content        []RAGEvent `json:"content"`
}

type RAGEvent struct {
	Event       string          `json:"event"`
	EventStatus string          `json:"event_status"`
	EventID     string          `json:"event_id"`
	EventType   string          `json:"type"`
	Text        json.RawMessage `json:"text"`
}

type RAGAnswer struct {
	Answer         string
	ConversationID string
	Events         []RAGEvent
}

func (t *RAGAnswer) transform(res *RAGRunResponse) {
	t.Answer = res.Result.Answer
	t.ConversationID = res.Result.ConversationID
	t.Events = res.Result.Content
}

// RAGIterator  定义RAGIterator流式/非流式统一的输出接口
// 迭代器初始状态可迭代,如果error返回不为空则代表迭代结束，对应如下两种情况：
// 1. 如果error为eoi，则代表迭代正常结束
// 2. 如果error不为空且不为eoi，则代表迭代异常
type RAGIterator interface {
	Next() (*RAGAnswer, error)
}

type RAGStreamIterator struct {
	body      io.ReadCloser
	p         *parser.Parser
	eof       bool
	closed    bool
	requestID string
}

func (t *RAGStreamIterator) Next() (*RAGAnswer, error) {
	for {
		if t.eof {
			return nil, io.EOF
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
		var resp RAGRunResponse
		if err := json.Unmarshal([]byte(event.Data), &resp); err != nil {
			return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
		}
		answer := &RAGAnswer{}
		answer.transform(&resp)
		return answer, nil
	}
}

type RAGOnceIterator struct {
	body      io.ReadCloser
	eoi       bool
	requestID string
}

func (t *RAGOnceIterator) Next() (*RAGAnswer, error) {
	if t.eoi {
		return nil, io.EOF
	}
	data, err := io.ReadAll(t.body)
	if err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	defer t.body.Close()
	var resp RAGRunResponse
	if err := json.Unmarshal(data, &resp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	t.eoi = true
	answer := &RAGAnswer{}
	answer.transform(&resp)
	return answer, nil
}
