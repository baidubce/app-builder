# Client应用调用官方组件

## 简介 

Agent是基于线上Agent应用的问答组件，可以使用该组件利用线上Agent应用进行问答，同时可以在线上为Client应用添加组件，丰富Agent能力。

## Agent添加Components官方组件

整体使用流程包括以下两个环节：

1. 在[百度智能云千帆AppBuilder官网](https://cloud.baidu.com/product/AppBuilder)创建并发布应用(在创建应用时可添加官方组件)、获取应用ID、获取密钥
2. 引用AppBuilderSDK代码，初始化AppBuilderClient实例、创建会话、上传文档（可选）、执行对话

## 示例

- 接下来将展示创建一个机票查询Agent应用，并添加官方组件。

### 创建应用

- 创建应用并添加自己的角色指令，并按照自己的需求设置模型、记忆功能等参数
![](https://bj.bcebos.com/v1/appbuilder-sdk-components/%E5%88%9B%E5%BB%BA%E8%88%AA%E7%8F%AD%E6%9F%A5%E8%AF%A2%E5%BA%94%E7%94%A8.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-12-17T03%3A51%3A31Z%2F-1%2Fhost%2Fde4a26a46469066111552bf91d50202433ef1cdd89f4945e7924ad11de38fb36)

### 添加官方组件

- 添加官方组件航班查询组件
![](https://bj.bcebos.com/v1/appbuilder-sdk-components/%E6%B7%BB%E5%8A%A0%E8%88%AA%E7%8F%AD%E6%9F%A5%E8%AF%A2%E6%8C%87%E4%BB%A4.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-12-17T03%3A52%3A17Z%2F-1%2Fhost%2F9dfcafb04d9e5992a4feda63f58ffe2211afb01b1e7b0f4f3ec4822ba840562c)

### 发布应用并调用

- 完成应用设置,并发布应用，接下来就可以调用添加了官方组件的Client应用了，应用的具体调用方法请参考[Agent应用基础知识](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/BasicKnowledge/agent.md)


