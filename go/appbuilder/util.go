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
	"bufio"
	"fmt"
	"io"
	"net/http"
)

type SSEEvent struct {
	LastEventID string
	Type        string
	Data        string
}

func checkHTTPResponse(rsp *http.Response) (string, error) {
	requestID := rsp.Header.Get("X-Appbuilder-Request-Id")
	if rsp.StatusCode == http.StatusOK {
		return requestID, nil
	}

	data, err := io.ReadAll(rsp.Body)
	if err != nil {
		return requestID, err
	}
	return requestID, fmt.Errorf("http status code is %d, content is %s", rsp.StatusCode, string(data))
}

func NewSSEReader(bufSize int, reader *bufio.Reader) *sseReader {
	buf := make([]byte, bufSize)
	return &sseReader{reader: reader, buf: buf, size: 0, cap: bufSize}
}

type sseReader struct {
	reader *bufio.Reader
	buf    []byte
	size   int
	cap    int
}

func (t *sseReader) ReadMessageLine() ([]byte, error) {
	t.size = 0
	line, isPrefix, err := t.reader.ReadLine()
	if err != nil {
		return nil, err
	}
	for isPrefix {
		t.size += copy(t.buf[t.size:], line)
		line, isPrefix, err = t.reader.ReadLine()
	}
	if len(line)+t.size > t.cap {
		panic("overflow buffer")
	}
	t.size += copy(t.buf[t.size:], line)
	// 读取空行
	t.reader.ReadLine()
	return t.buf[0:t.size], nil
}
