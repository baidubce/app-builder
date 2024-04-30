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
	"errors"
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
	return &sseReader{reader: reader, buf: buf}
}

type sseReader struct {
	reader *bufio.Reader
	buf    []byte
}

func (t *sseReader) ReadMessageLine() ([]byte, error) {
	size := 0
	for {
		line, isPrefix, err := t.reader.ReadLine()
		if err != nil {
			return nil, err
		}
		if len(line)+size > cap(t.buf) {
			panic("buffer overflow")
		}
		size += copy(t.buf[size:], line)
		if !isPrefix {
			break
		}
	}
	// 读取空行
	line, _, err := t.reader.ReadLine()
	if err != nil || len(line) != 0 {
		size += copy(t.buf[size:], line)
		return nil, errors.New(string(t.buf[0:size]))
	}
	return t.buf[0:size], nil
}
