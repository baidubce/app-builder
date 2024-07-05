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

const (
	GatewayURL            = "GATEWAY_URL"
	GatewayURLV2          = "GATEWAY_URL_V2"
	SecretKey             = "APPBUILDER_TOKEN"
	ConsoleOpenAPIVersion = "CONSOLE_OPENAPI_VERSION"
	ConsoleOpenAPIPrefix  = "CONSOLE_OPENAPI_PREFIX"
	SecretKeyPrefix       = "SECRET_KEY_PREFIX"

	DefaultSecretKeyPrefix       = "Bearer"
	DefaultGatewayURL            = "https://appbuilder.baidu.com"
	DefaultGatewayURLV2          = "https://qianfan.baidubce.com"
	DefaultConsoleOpenAPIVersion = "/v2"
	DefaultConsoleOpenAPIPrefix  = ""
)

type SDKConfig struct {
	GatewayURL            string
	GatewayURLV2          string
	ConsoleOpenAPIVersion string
	ConsoleOpenAPIPrefix  string
	SecretKey             string
	HTTPClient            HTTPClient // custom HTTP Client, optional
	logger                zerolog.Logger
}

func NewSDKConfig(gatewayURL, secretKey string) (*SDKConfig, error) {
	gatewayURL = getEnvWithDefault(GatewayURL, gatewayURL, DefaultGatewayURL)
	gatewayURLV2 := getEnvWithDefault(GatewayURLV2, "", DefaultGatewayURLV2)
	openAPIVersion := getEnvWithDefault(ConsoleOpenAPIVersion, "", DefaultConsoleOpenAPIVersion)
	openAPIPrefix := getEnvWithDefault(ConsoleOpenAPIPrefix, "", DefaultConsoleOpenAPIPrefix)

	secretKey = getEnvWithDefault(SecretKey, secretKey, "")
	if len(secretKey) == 0 {
		log.Error().Msg("secret key is empty")
	}
	secretKeyPrefix := getEnvWithDefault(SecretKeyPrefix, "", DefaultSecretKeyPrefix)
	if !strings.HasPrefix(secretKey, secretKeyPrefix) {
		secretKey = secretKeyPrefix + " " + secretKey
	}

	sdkConfig := &SDKConfig{
		GatewayURL:            gatewayURL,
		GatewayURLV2:          gatewayURLV2,
		ConsoleOpenAPIVersion: openAPIVersion,
		ConsoleOpenAPIPrefix:  openAPIPrefix,
		SecretKey:             secretKey,
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

func getEnvWithDefault(key, paramValue, defaultValue string) string {
	if paramValue != "" {
		return paramValue
	}

	v := os.Getenv(key)
	if v == "" {
		return defaultValue
	}
	return v
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
	platform := os.Getenv("APPBUILDER_SDK_PLATFORM")
	if platform == "" {
		platform = "unknown"
	}
	header.Set("X-Appbuilder-Origin", "appbuilder_sdk")
	header.Set("X-Appbuilder-Sdk-Config", "{\"appbuilder_sdk_version\":\"0.9.0\",\"appbuilder_sdk_language\":\"go\",\"appbuilder_sdk_platform\":\""+platform+"\"}")
	header.Set("X-Appbuilder-Request-Id", uuid.New().String())
	return header
}

func (t *SDKConfig) ServiceURL(suffix string) (*url.URL, error) {
	absolutePath, err := url.JoinPath(t.GatewayURL, suffix)
	if err != nil {
		return nil, err
	}
	return t.formatURL(absolutePath)
}

// ServiceURLV2 适配OpenAPI，当前仅AppbuilderClient使用
func (t *SDKConfig) ServiceURLV2(suffix string) (*url.URL, error) {
	absolutePath, err := url.JoinPath(t.GatewayURLV2, t.ConsoleOpenAPIPrefix, t.ConsoleOpenAPIVersion, suffix)
	if err != nil {
		return nil, err
	}
	return t.formatURL(absolutePath)
}

func (t *SDKConfig) formatURL(absolutePath string) (*url.URL, error) {
	t.logger.Debug().Msgf("Service URL %s", absolutePath)
	url, err := url.Parse(absolutePath)
	if err != nil {
		return nil, err
	}
	return url, nil
}

func (t *SDKConfig) BuildCurlCommand(req *http.Request) {
	curlCmd := fmt.Sprintf("curl -X %s -L '%v' \\\n", req.Method, req.URL.String())

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
	} else if req.Method == "GET" || req.Method == "DELETE" {
		curlCmd = strings.TrimSuffix(curlCmd, " \\\n")
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
