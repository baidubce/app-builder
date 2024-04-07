# AppBuilder ConsoleSDK
提供Go语言版本的ConsoleSDK，支持调用AgentBuilder、Dataset、RAG等接口能力，方便用户快速集成

##  安装使用

```shell
go get github.com/baidubce/app-builder/appbuilder-go
````

## AgentBuilder使用示例

```go
import "appbuilder"
func main() {
	// 使用环境变量
	os.Setenv("APPBUILDER_TOKEN", "")
	os.Setenv("GATEWAY_URL", "")
	// 或直接通过参数传递
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new sdk failed: ", err)
		return
	}
	// 初始化实例
	agentBuilder, err := appbuilder.NewAgentBuilder("", config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := agentBuilder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ",err)
		return
	}
	// 上传文件
	fileID, err := agentBuilder.UploadLocalFile(conversationID, "/path/to/file")
	if err != nil {
		fmt.Println("upload local file failed:", err)
		return
	}
	// 执行对话
	i, err := agentBuilder.Run(conversationID, "描述简历中的候选人情况", []string{fileID}, true)
	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}
	totalAnswer := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			if ev.ContentType == TextContentType {
				_ = ev.Detail.(TextDetail)
			} else if ev.ContentType == CodeContentType {
				_ = ev.Detail.(CodeDetail)
			} else if ev.ContentType == ImageContentType {
				_ = ev.Detail.(ImageDetail)
			} else if ev.ContentType == RAGContentType {
				_= ev.Detail.(RAGDetail)
			} else if ev.ContentType == FunctionCallContentType {
				_ = ev.Detail.(FunctionCallDetail)
			} else if ev.ContentType == AudioContentType {
				_= ev.Detail.(AudioDetail)
			} else if ev.ContentType == VideoContentType {
				_= ev.Detail.(VideoDetail)
			} else if ev.ContentType == StatusContentType {
			} else { // 默认是json.RawMessage
				_= ev.Detail.(json.RawMessage)
			}
		}
	}
	fmt.Println(totalAnswer)
}
```

## RAG使用示例
```go
func main() {
	config, err := NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
	}
	// 初始化RAG实例
	rag, err := NewRAG("", config)
	if err != nil {
		fmt.Println("new rag instance failed:", err)
		return
	}
	// 执行流式对话
	i, err := rag.Run("", "面试需要注意的细节", true)
	if err != nil {
		fmt.Println("run failed:", err)
		return 
    }   
	totalAnswer := ""
	// 迭代返回结果
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer = totalAnswer + answer.Answer
	}
	fmt.Println(totalAnswer)
}
```
## Dataset使用示例
```go
func main() {
	// 初始化config
	config, err := NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new client config failed: ", err)
		return
	}
	
	// 初始化dataset实例
	dataset, _ := NewDataset(config)
	
	// 创建dataset 
	datasetID, err := dataset.Create("测试集合")
	if err != nil {
		fmt.Println("new dataset failed: ", err)
		return
	}
	// 上传文档
	documentID, err := dataset.UploadLocalFile(datasetID, "/Users/zhangxiaoyu15/Desktop/cv.pdf")
	if err != nil {
		fmt.Println("upload file failed: ", err)
		return
	}
	// 获取第一页最多不超过10篇的文档
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