# AppBuilder ConsoleSDK
提供Go语言版本的ConsoleSDK，支持调用AgentBuilder、Dataset、RAG等接口能力，方便用户快速集成

##  安装使用
支持Go 1.18.1以上版本

```shell
go get github.com/baidubce/app-builder/go/appbuilder
````

## AgentBuilder使用示例

```go
func main() {
        // 使用环境变量
        // 或直接通过参数传递
		os.Setenv("APPBUILDER_TOKEN", "")
		os.Setenv("GATEWAY_URL", "")
        config, err := appbuilder.NewSDKConfig("", "")
        if err != nil {
                fmt.Println("new sdk failed: ", err)
                return
        }
        // 初始化实例
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
                        } else { // 默认是json.RawMessage
                                detail := ev.Detail.(appbuilder.DefaultDetail)
                                fmt.Println(detail)
                        }
                }
        }
        fmt.Println(totalAnswer)
}

```

## Dataset使用示例
```go

func main() {
        config, err := appbuilder.NewSDKConfig("", "")
        if err != nil {
                fmt.Println("new client config failed: ", err)
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
        // 获取第一页最多不超过10篇的文档
        resp, err := dataset.ListDocument(datasetID, 1, 10, "")
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

## RAG使用示例
```go
func main() {
        config, err := appbuilder.NewSDKConfig("", "")
        if err != nil {
                fmt.Println("new config failed: ", err)
        }
        // 初始化RAG实例
        rag, err := appbuilder.NewRAG("", config)
        if err != nil {
                fmt.Println("new rag instance failed:", err)
                return
        }
        // 执行流式对话
        i, err := rag.Run("", "北京有多少小学生", true)
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