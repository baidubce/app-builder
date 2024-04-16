# AppBuilder ConsoleSDK
支持调用AgentBuilder、Dataset、RAG等应用接口能力，方便用户快速集成

##  安装使用
支持Go 1.18.1以上版本

```shell
go get github.com/baidubce/app-builder/go/appbuilder
````

## 1. AgentBuilder使用示例

```go
package main

import (
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://appbuilder.baidu.com
	os.Setenv("GATEWAY_URL", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	agentBuilder, err := appbuilder.NewAgentBuilder(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := agentBuilder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}
	// 上传文件
	fileID, err := agentBuilder.UploadLocalFile(conversationID, "/path/to/cv.pdf")
	if err != nil {
		fmt.Println("upload local file failed:", err)
		return
	}
	// 执行流式对话
	i, err := agentBuilder.Run(conversationID, "描述简历中的候选人情况", []string{fileID}, true)
	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}

	completedAnswer := ""
	var answer *appbuilder.AgentBuilderAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		completedAnswer = completedAnswer + answer.Answer
		for _, ev := range answer.Events {
			if ev.ContentType == appbuilder.TextContentType {
				detail := ev.Detail.(appbuilder.TextDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.CodeContentType {
				detail := ev.Detail.(appbuilder.CodeDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.ImageContentType {
				detail := ev.Detail.(appbuilder.ImageDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.RAGContentType {
				detail := ev.Detail.(appbuilder.RAGDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.FunctionCallContentType {
				detail := ev.Detail.(appbuilder.FunctionCallDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.AudioContentType {
				detail := ev.Detail.(appbuilder.AudioDetail)
				fmt.Println(detail.Audio)
			} else if ev.ContentType == appbuilder.VideoContentType {
				detail := ev.Detail.(appbuilder.VideoDetail)
				fmt.Println(detail)
			} else if ev.ContentType == appbuilder.StatusContentType {
			} else { // 默认detail
				detail := ev.Detail.(appbuilder.DefaultDetail)
				fmt.Println(detail)
			}
		}
	}
	// 迭代正常结束err应为io.EOF
	if errors.Is(err, io.EOF) {
		fmt.Println("run success")
		fmt.Println("智能体回答内容： ", completedAnswer)
	} else {
		fmt.Println("run failed:", err)
	}
}

```

## 2. Dataset使用示例
```go
package main

import (
	"fmt"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"

)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://appbuilder.baidu.com
	os.Setenv("GATEWAY_URL", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化dataset实例
	dataset, _ := appbuilder.NewDataset(config)
	// 创建dataset
	datasetID, err := dataset.Create("name")
	if err != nil {
		fmt.Println("create dataset failed: ", err)
		return
	}
	// 上传文档
	documentID, err := dataset.UploadLocalFile(datasetID, "/Users/zhangxiaoyu15/Desktop/cv.pdf")
	if err != nil {
		fmt.Println("upload file failed: ", err)
		return
	}
	// 获取数据集下第一页不超过10篇文档
	_, err = dataset.ListDocument(datasetID, 1, 10, "")
	if err != nil {
		fmt.Println("list document failed: ", err)
		return
	}
	// 删除文档
	if err := dataset.DeleteDocument(datasetID, documentID); err != nil {
		fmt.Println("delete document failed: ", err)
		return
	}
}
```

## 3. RAG使用示例
<span style="color:red">⚠️本示例仅适用于2024-04-02之前创建的历史RAG应用，最新创建的智能体应用，请参考上方**AgentBuilder**调用示例。
</span>


```go
package main

import (
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://appbuilder.baidu.com
	os.Setenv("GATEWAY_URL", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化RAG实例
	appID := "请填写正确的应用ID"
	rag, err := appbuilder.NewRAG(appID, config)
	if err != nil {
		fmt.Println("new rag instance failed:", err)
		return
	}
	// 执行流式对话
	i, err := rag.Run("", "", true)
	if err != nil {
		fmt.Println("run failed:", err)
		return
	}
	completedAnswer := ""
	// 迭代返回结果
	var answer *appbuilder.RAGAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		completedAnswer = completedAnswer + answer.Answer
	}
	// 迭代正常结束err应为io.EOF
	if errors.Is(err, io.EOF) {
		fmt.Println("run success")
		fmt.Println("RAG智能体回答内容： ", completedAnswer)
	} else {
		fmt.Println("run failed:", err)
	}
}
```