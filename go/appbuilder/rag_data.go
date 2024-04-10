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
	"strings"
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

// RAGIterator 定义RAG流式/非流式迭代器接口
// 初始状态可迭代,如果返回error不为空则代表迭代结束，
// error为io.EOF，则代表迭代正常结束，其它则为异常结束
type RAGIterator interface {
	// Next 获取处理结果，如果返回error不为空，迭代器自动失效，不允许再调用此方法
	Next() (*RAGAnswer, error)
}

type RAGStreamIterator struct {
	requestID string
	r         *sseReader
	body      io.ReadCloser
}

func (t *RAGStreamIterator) Next() (*RAGAnswer, error) {
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
		var resp RAGRunResponse
		resp.Code = -1
		if err := json.Unmarshal(data[5:], &resp); err != nil {
			t.body.Close()
			return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
		}
		if resp.Code != 0 {
			t.body.Close()
			return nil, fmt.Errorf("requestID=%s, body=%s", t.requestID, string(data))
		}
		answer := &RAGAnswer{}
		answer.transform(&resp)
		return answer, nil
	}
	// 非SSE格式关闭连接，并返回数据
	t.body.Close()
	return nil, fmt.Errorf("requestID=%s, body=%s", t.requestID, string(data))
}

// RAGOnceIterator 非流式返回时对应的迭代器，只可迭代一次
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
	resp.Code = -1
	if err := json.Unmarshal(data, &resp); err != nil {
		return nil, fmt.Errorf("requestID=%s, err=%v", t.requestID, err)
	}
	if resp.Code != 0 {
		t.body.Close()
		return nil, fmt.Errorf("requestID=%s, body=%s", t.requestID, string(data))
	}
	t.eoi = true
	answer := &RAGAnswer{}
	answer.transform(&resp)
	return answer, nil
}
