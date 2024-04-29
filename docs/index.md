# AppBuilder
AppBuilder面向开发者提供AI原生应用一站式开发工具，包括基础云资源、AI能力引擎、千帆大模型以及相关能力组件，提升AI原生应用开发效率。

百度智能云千帆 AppBuilder 在提供零代码、低代码的AI原生应用搭建功能之外，也提供全代码灵活开发与集成能力。基于官方 API/SDK，开放丰富的组件服务，提供具备强大对话、思考及工具调用能力的 Agent 应用框架。

封装程度由高至低，AppBuilder 提供了三种类型的SDK
| 分类   | 场景及使用方式   | 百度云文档链接         | SDK 文档链接|
|--------|--------|------------|------------|
| 端到端应用 | 在 AppBuilder 产品界面上通过零代码、低代码方式创建的 AI 原生应用，支持通过应用 API/SDK 进行调用 | [应用API及SDK](https://cloud.baidu.com/doc/AppBuilder/s/Flpv3oxup) | [AppBuilder Client SDK](./agent_builder.md) |
| 代码态智能体 | 基于 Assistants API，可通过全代码形式创建和调试专属智能体（Agent） | [AssistantAPI](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben) | [AssistantSDK](./assistant_sdk.md) |
| 工具组件 | 基于组件 SDK，可调用包括大模型组件、AI能力组件等在内的多种组件 | [组件SDK](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz) | [组件列表](../appbuilder/core/components) |


以下列出用户常用组件的说明文档:

## 一级文档目录
1. [获取模型列表](get_model_list.md)
2. [AppBuilder - Agent应用 AppBuilder Client SDK](appbuilder_client.md)
3. [AppBuilder - Dataset知识库SDK](dataset.md)
4. [AppBuilder - RAG应用 SDK](rag.md)
5. [AppBuilder - Assistant SDK](assistant_sdk.md)



