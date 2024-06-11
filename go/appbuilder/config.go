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
	"io"
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

	logLevel := strings.ToLower(os.Getenv("APPBUILDER_LOGLEVEL"))
	zerologLevel := zerolog.InfoLevel
	switch logLevel {
	case "debug":
		zerologLevel = zerolog.DebugLevel
	case "warning":
		zerologLevel = zerolog.WarnLevel
	case "error":
		zerologLevel = zerolog.ErrorLevel
	default:
		zerologLevel = zerolog.InfoLevel
	}

	sdkConfig := &SDKConfig{GatewayURL: gatewayURL, GatewayURLV2: gatewayURLV2, SecretKey: secretKey}

	logFile := os.Getenv("APPBUILDER_LOGFILE")
	if len(logFile) > 0 {
		f, err := os.OpenFile(logFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
		if err != nil {
			sdkConfig.logger = zerolog.New(os.Stdout).Level(zerologLevel)
		} else {
			sdkConfig.logger = zerolog.New(f).Level(zerologLevel)
		}
	} else {
		sdkConfig.logger = zerolog.New(os.Stdout).Level(zerologLevel)
	}

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

func (t *SDKConfig) BuildCurlCommand(req *http.Request) {
	curlCmd := fmt.Sprintf("curl -L %v \\\n", req.URL.String()) // add -L flag for following redirects

	for k, v := range req.Header {
		header := fmt.Sprintf("-H '%v: %v' \\\n", k, v[0])
		curlCmd = fmt.Sprintf("%v %v", curlCmd, header)
	}

	if req.Method == "POST" {
		bodyBytes, err := io.ReadAll(req.Body)
		if err != nil {
			t.logger.Error().Msgf("Failed to read request body: %v", err)
			return
		}
		req.Body.Close()
		req.Body = io.NopCloser(strings.NewReader(string(bodyBytes)))

		body := fmt.Sprintf("-d '%v'", string(bodyBytes))
		curlCmd = fmt.Sprintf("%v %v", curlCmd, body)
	}
	if t.logger.GetLevel() == zerolog.DebugLevel {
		logFile := os.Getenv("APPBUILDER_LOGFILE")
		if len(logFile) > 0 {
			file, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
			if err != nil {
				fmt.Println("Failed to open log file:", err)
				return
			}
			defer file.Close()

			originalStdout := os.Stdout
			defer func() { os.Stdout = originalStdout }()
			os.Stdout = file
		}
		fmt.Println("\n" + curlCmd + "\n")
	}
}
