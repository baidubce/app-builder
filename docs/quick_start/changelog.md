# 版本更新记录

* **2023.12.19 v0.1.0版本发布**：[Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.1.0)
  * 初始版本发布，基础云组件支持包括BES；AI能力引擎语音、视觉类10个能力，大模型相关RAG、文本生成能力19个。
* **2024.01.03 v0.2.0版本发布** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.2.0)
  * 核心升级点GBI相关组件新增，v0.1.0遗留问题修复
* **2024.01.26 v0.3.0版本发布** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.3.0)
  * 新增组件：新增了百度搜索rag组件(RAGwithBaiduSearch)。[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/rag_with_baidusearch.ipynb)
  * 模型列表获取：与千帆大模型平台模型名打通，可动态获取当前账号模型名，并在组件中使用[获取模型列表](/docs/basic_module/get_model_list.md)
  * 可通过官方镜像开发和运行实例代码[二次开发](/docs/develop_guide/README.md)
* **2024.02.27 v0.4.0版本发布** [Release Note](https://github.com/baidubce/app-builder/releases/tag/0.4.0)
  * AppBuilder Console SDK发布[知识集合Cookbook](/cookbooks/end2end_application/console_dataset.ipynb)，[RAG调用Cookbook](/cookbooks/end2end_application/rag/rag.ipynb)
  * 大模型组件新增：Excel2Figure(基于Excel信息画图表)
  * AI能力引擎组件新增&更新：植物识别、动物识别、表格文字识别V2、手写文字识别、二维码识别、身份证混贴识别、文档矫正识别、图像内容理解、流式TTS
  * AgentRuntime：新增[Cookbook](/cookbooks/components/agent_runtime.ipynb)
* **2024.03.13 v0.4.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.4.1)
  * 支持以下功能进行FunctionCall调用：动植物识别、表格文字识别、条形码及二维码识别、身份证混贴识别、手写文字识别、text2image、excel2figure
* **2024.03.20 v0.5.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.5.0)
  * AgentBuilder ConsoleSDK发布 [Agent调用CookBook](/cookbooks/end2end_application/agent/appbuilder_client.ipynb)
  * AI能力引擎组件新增：向量检索-VDB
  * 支持以下功能进行FunctionCall调用并新增[CookBook](/cookbooks/components/general_ocr.ipynb)：文本翻译-通用版、通用物体和场景识别-高级版、通用文字识别-高精度版、短语音识别-极速版
* **2024.03.21 v0.5.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.5.1)
  * 问题修复：修复了在Python 3.8 及以下环境无法使用AgentBuilder ConsoleSDK的问题。同时，在即将发布的0.6.0版本中，将不再提供对Python 3.8及以下环境的支持，请升级Python版本到3.9
* **2024.04.12 v0.6.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.6.0)
  * AppBuilder Console SDK 支持 JAVA 语言 [AppBuilder Java ConsoleSDK](/java/)
  * AppBuilder Console SDK 支持 GO 语言 [AppBuilder GO ConsoleSDK](/go/)
  * 首页README更新，提供免费的公共试用TOKEN，方便开发者快速体验
* **2024.04.30 v0.7.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.7.0)
  * 提供Assistant SDK 功能，新增 [CookBook](/cookbooks/pipeline/assistant_function_call.ipynb)，包含流程编排与FunctionCall，搭建个性化Agent应用
  * AgentBuilder组件更名为 AppBuilderClient, 后续版本将放弃对 `AgentBuilder` 的后向兼容支持
  * 首页Readme与文档结构优化
* **2024.05.21 v0.7.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.7.1)
  * 更新Assistant SDK 功能，为assistants/threads/messages/runs/files模块提供了完整的增删改查api, 新增`appbuilder.AssistantEventHandler`与`appbuilder.assistant.threads.runs.stream_run_with_handler`方法，更好的支持Assistant的流式调用
  * 支持AppBuilder Client通过chainlit进行可视化的服务化部署
  * 优化SDK的报错信息提示，方便开发者进行debug
  * 修复文档格式转换组件的域名错误问题
* **2024.06.11 v0.8.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.8.0)
  * 提供功能更强大的Debug模式
  * 支持AppBuilder Client通过chainlit进行可视化的服务化部署
  * 多个组件进行了效果优化与说明文档更新
* **2024.06.28 v0.9.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.0)
  * Python/Go/Jave Console SDK 上新，支持Token用量返回，支持`get_app_list`， 支持`KnowledgeBase`功能
  * 新增AppBuilder-SDK Depoly功能，支持用户使用SDK快速部署本地组件orAgent应用到百度智能云，并对外提供服务
  * 更新SDK超参，支持SDK在私有化部署环境的使用
  * 更新口语化组件，优化效果