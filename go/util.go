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
	"errors"
	"fmt"
	"io"
	"net/http"

	"github.com/baidubce/app-builder/appbuilder-go/internal/parser"
)

var eoi = errors.New("iterator exhausted")

type SSEEvent struct {
	LastEventID string
	Type        string
	Data        string
}

func readNext(p *parser.Parser) (SSEEvent, error) {
	ev, dirty := SSEEvent{}, false
	for f := (parser.Field{}); p.Next(&f); {
		switch f.Name {
		case parser.FieldNameData:
			ev.Data += f.Value + "\n"
			dirty = true
		case parser.FieldNameEvent:
			ev.Type = f.Value
			dirty = true
		case parser.FieldNameID:
			dirty = true
		case parser.FieldNameRetry:
			dirty = true
		default:
			return ev, nil
		}
	}
	err := p.Err()
	if dirty && err == io.EOF {
		return ev, err
	}
	return SSEEvent{}, err
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
