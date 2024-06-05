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
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/google/uuid"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

type SDKConfig struct {
	GatewayURL   string
	GatewayURLV2 string
	SecretKey    string
	logger       zerolog.Logger
}

func NewSDKConfig(gatewayURL, secretKey string) (*SDKConfig, error) {
	if len(gatewayURL) == 0 {
		gatewayURL = os.Getenv("GATEWAY_URL")
	}
	if len(gatewayURL) == 0 {
		gatewayURL = "https://appbuilder.baidu.com"
	}

	gatewayURLV2 := os.Getenv("GATEWAY_URL_V2")
	if gatewayURLV2 == "" {
		gatewayURLV2 = "https://qianfan.baidubce.com"
	}

	if len(secretKey) == 0 {
		secretKey = os.Getenv("APPBUILDER_TOKEN")
	}
	if len(secretKey) == 0 {
		log.Error().Msg("secret key is empty")
	}
	if !strings.HasPrefix(secretKey, "Bearer ") {
		secretKey = "Bearer " + secretKey
	}

	logLevel := os.Getenv("APPBUILDER_LOGLEVEL")
	zerologLevel := zerolog.InfoLevel
	if strings.ToLower(logLevel) == "debug" {
		zerologLevel = zerolog.DebugLevel
	}

	sdkConfig := &SDKConfig{GatewayURL: gatewayURL, GatewayURLV2: gatewayURLV2, SecretKey: secretKey}
	sdkConfig.logger = zerolog.New(os.Stdout).Level(zerologLevel)

	return sdkConfig, nil
}

func (t *SDKConfig) AuthHeader() http.Header {
	header := t.authHeader()
	header.Set("X-Appbuilder-Authorization", t.SecretKey)
	t.logger.Debug().Msgf("Auth Header %v", header)
	return header
}

// AuthHeaderV2 适配OpenAPI，当前仅AgentBuilder使用
func (t *SDKConfig) AuthHeaderV2() http.Header {
	header := t.authHeader()
	header.Set("Authorization", t.SecretKey)
	t.logger.Debug().Msgf("Auth Header %v", header)
	return header
}

func (t *SDKConfig) authHeader() http.Header {
	header := make(http.Header)
	header.Set("X-Appbuilder-Origin", "appbuilder_sdk")
	header.Set("X-Appbuilder-Sdk-Config", "{\"appbuilder_sdk_version\":\"0.8.0\",\"appbuilder_sdk_language\":\"go\"}")
	header.Set("X-Appbuilder-Request-Id", uuid.New().String())
	return header
}

func (t *SDKConfig) ServiceURL(suffix string) (*url.URL, error) {
	return t.serviceURL(t.GatewayURL, suffix)
}

// ServiceURLV2 适配OpenAPI，当前仅AgentBuilder使用
func (t *SDKConfig) ServiceURLV2(suffix string) (*url.URL, error) {
	return t.serviceURL(t.GatewayURLV2, suffix)
}

func (t *SDKConfig) serviceURL(gateway, suffix string) (*url.URL, error) {
	absolutePath := gateway + suffix
	t.logger.Debug().Msgf("Service URL %s", absolutePath)
	url, err := url.Parse(absolutePath)
	if err != nil {
		return nil, err
	}
	return url, nil
}
