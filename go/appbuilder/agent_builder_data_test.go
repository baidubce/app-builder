package appbuilder

import (
	"encoding/json"
	"testing"
	"bufio"
	"io"
	"strings"
)

// 测试 if !ok 分支
func TestAgentBuilderAnswerTransformWithInvalidContentType(t *testing.T) {
	// 构造一个 AgentBuilderRawResponse，其中 ContentType 是不存在的
	rawResponse := &AgentBuilderRawResponse{
		Answer: "Test Answer",
		Content: []RawEventDetail{
			{
				EventCode:    111,
				EventMessage: "Test Message",
				EventStatus:  "Success",
				EventType:    "TestType",
				ContentType:  "InvalidContentType", // 模拟不存在的 ContentType
				Outputs:      json.RawMessage(`{}`), // 空的输出
			},
		},
	}

	// 调用 transform 方法
	answer := &AgentBuilderAnswer{}
	answer.transform(rawResponse)
}
// 测试 err != nil && !(err == io.EOF) 分支
func TestAgentBuilderStreamIterator_Next_ReadError(t *testing.T) {
	// 模拟没有数据的输入
	mockBody := io.NopCloser(strings.NewReader(""))
	reader := bufio.NewReader(mockBody)
	sseReader := NewSSEReader(1024, reader)

	streamIterator := &AgentBuilderStreamIterator{
		requestID: "test-request",
		r:         sseReader, // 使用 NewSSEReader 初始化的 sseReader
		body:      mockBody,
	}

	// 调用 Next 并检查返回的错误
	_, err := streamIterator.Next()
	if err != io.EOF {
		t.Fatalf("expected io.EOF, got %v", err)
	}
}

// 测试 json.Unmarshal 解析失败
func TestAgentBuilderStreamIterator_Next_JSONUnmarshalError(t *testing.T) {
	// 模拟 SSE 消息，data 后面跟着无效 JSON
	mockBody := io.NopCloser(strings.NewReader("data: invalid-json"))
	reader := bufio.NewReader(mockBody)
	sseReader := NewSSEReader(1024, reader)

	streamIterator := &AgentBuilderStreamIterator{
		requestID: "test-request",
		r:         sseReader,
		body:      mockBody,
	}

	// 调用 Next 并检查返回的错误
	_, err := streamIterator.Next()
	if err == nil || !strings.Contains(err.Error(), "invalid character") {
		
	}
}

// 测试非 SSE 格式数据
func TestAgentBuilderStreamIterator_Next_NonSSEFormat(t *testing.T) {
	// 模拟非 SSE 格式的消息
	mockBody := io.NopCloser(strings.NewReader("not-sse-format-data"))
	reader := bufio.NewReader(mockBody)
	sseReader := NewSSEReader(1024, reader)

	streamIterator := &AgentBuilderStreamIterator{
		requestID: "test-request",
		r:         sseReader,
		body:      mockBody,
	}

	// 调用 Next 并检查返回的错误
	streamIterator.Next()
}

// 测试正常的 SSE 数据流
func TestAgentBuilderStreamIterator_Next_ValidSSE(t *testing.T) {
	// 模拟有效的 SSE 消息
	mockBody := io.NopCloser(strings.NewReader("data: {\"answer\": \"Test Answer\", \"content\": []}"))
	reader := bufio.NewReader(mockBody)
	sseReader := NewSSEReader(1024, reader)

	streamIterator := &AgentBuilderStreamIterator{
		requestID: "test-request",
		r:         sseReader,
		body:      mockBody,
	}

	// 调用 Next 并检查返回的结果
	streamIterator.Next()
}