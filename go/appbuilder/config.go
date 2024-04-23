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
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"
	"github.com/google/uuid"
)

type SDKConfig struct {
	GatewayURL string
	SecretKey  string
}

func NewSDKConfig(gatewayURL, secretKey string) (*SDKConfig, error) {
	if len(gatewayURL) == 0 {
		gatewayURL = os.Getenv("GATEWAY_URL")
	}
	if len(gatewayURL) == 0 {
		gatewayURL = "https://appbuilder.baidu.com"
	}
	if len(secretKey) == 0 {
		secretKey = os.Getenv("APPBUILDER_TOKEN")
	}
	if len(secretKey) == 0 {
		fmt.Errorf("secret key is empty")
	}
	if !strings.HasPrefix(secretKey, "Bearer ") {
		secretKey = "Bearer " + secretKey
	}

	return &SDKConfig{GatewayURL: gatewayURL, SecretKey: secretKey}, nil
}

func (t *SDKConfig) AuthHeader() http.Header {
	header := make(http.Header)
	header.Set("X-Appbuilder-Authorization", t.SecretKey)
	header.Set("X-Appbuilder-Origin", "appbuilder_sdk")
	header.Set("X-Appbuilder-Sdk-Config", "{\"appbuilder_sdk_version\":\"0.7.0\",\"appbuilder_sdk_language\":\"go\"}")
	header.Set("X-Appbuilder-Request-Id", uuid.NewV4().String())
	return header
}

func (t *SDKConfig) ServiceURL(suffix string) (*url.URL, error) {
	absolutePath := t.GatewayURL+ suffix
	url, err := url.Parse(absolutePath)
	if err != nil {
		return nil, err
	}
	return url, nil
}
