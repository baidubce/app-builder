<div align="center">
<img src='docs/image/logo.png' alt='logo' width='700' >
<br>

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.9+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)
</div>

<br>


## 什么是AppBuilder-SDK

`百度智能云千帆AppBuilder-SDK`是[百度智能云千帆AppBuilder](https://appbuilder.cloud.baidu.com/)面向AI原生应用开发者提供的一站式开发工具。

我们提供自底向上的：基础组件、流程编排、端到端应用 三类功能。使用百度智能云千帆AppBuilder-SDK，你可以：

- 配合百度智能云千帆AppBuilder平台[网页端](https://console.bce.baidu.com/ai_apaas/app)，分钟级在本地搭建包含百度工业实践的`端到端的AI原生应用`：Agent/RAG/工作流应用
- 配合 `基础组件` & `流程编排`，积木式搭建个性化的Assistant + FunctionCall应用
- 提供 `API调用` & `交互式窗口` 两种服务化部署方式，支持快速上云，平滑嵌入到你的产品中


##  如何安装

#### 百度智能云千帆AppBuilder-SDK 最新版本 0.7.0 (2024-04-30)

百度智能云千帆AppBuilder-SDK 更新记录&最新特性请查阅我们的[版本说明]()

- 我们推荐安装`Python`最新稳定版本

```bash
python3 -m pip install --upgrade appbuilder-sdk
```
- `Java` 及 `Go` 版本安装，以及通过`Docker`镜像使用，请查阅[安装说明]()


## 快速开始你的第一个AI原生应用

- 请在`>=3.9`的Python环境安装`appbuilder-sdk`后使用该端到端应用示例
- 示例中提供了试用Token，访问和QPS受限，正式使用请替换为您的个人Token
- 示例中的应用为：[地理小达人](https://appbuilder.baidu.com/s/x1tSF)，点击该连接在网页端试用

#### 代码示例

```python
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN为访问和QPS受限的试用TOKEN，正式使用请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# 从AppBuilder网页获取并传入应用ID，以下为地理小达人应用ID
app_id = "42eb211a-14b9-43d2-9fae-193c8760ef26"

app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_builder_client.create_conversation()

answer = app_builder_client.run(conversation_id, "中国的首都在哪里？春季天气怎么样？有什么适合玩的景点？")
print(answer.content)
```

#### 回答展示

> 中国的首都是**北京**^[2]^。
> 
> 春季的北京天气多变，早晚温差较大，出门还是要多带件外套。但是，这个季节是北京逛公园的好季节，玉兰花、桃花与迎春花等花卉盛开，为北京的春天增添了美丽的色彩^[1]^。
> 
> 适合玩的景点有：
> 1. **天坛公园**。天坛公园是明清两代的皇家祭祀场所，也是世界上现存规模最大的古代祭祀建筑群。
> 2. **故宫博物院**。故宫是中国古代建筑和文化的重要遗产，也是北京的一大旅游景点。
> 3. **长城**。长城是中国古代的一项伟大工程，也是北京周边的重要景点。
> 4. **颐和园**。颐和园是中国古代皇家园林，也是北京的一大旅游景点^[1]^。


**更多AI原生应用示例代码，请查阅 [CookBooks](./cookbooks/README.md)**，我们有以下cookbook推荐您优先阅读：
- 基础能力组件
    - [通用文字识别组件](/cookbooks/components/general_ocr.ipynb)
    - [基础组件服务化](/cookbooks/components/agent_runtime.ipynb)
- 流程编排
    - [Assistant SDK](/cookbooks/pipeline/assistant_function_call.ipynb)
- 端到端应用
    - [Agent应用](/cookbooks/agent_builder.ipynb)
    - [RAG应用](/cookbooks/end2end_application/rag/rag.ipynb)
    - [企业级问答系统](/cookbooks/end2end_application/rag/qa_system_2_dialogue.ipynb)


## 百度智能云千帆AppBuilder-SDK 能力全景图
<div align="center">
<img src='docs/image/structure-cn.png' alt='wechat' width='800' >
</div>


## 用户文档

- [快速开始](/docs/quick_start/README.md)
    - [安装说明](/docs/quick_start/install.md)
    - [版本说明](/docs/quick_start/changelog.md)
- [基础功能](/docs/basic_module/README.md)
    - [基础能力组件](/docs/basic_module/components.md)
    - [流程编排](/docs/basic_module/assistant_sdk.md)
    - [端到端应用](/docs/basic_module/appbuilder_client.md)
- [进阶实践](/docs/advanced_application/README.md)
    - [CookBooks](/cookbooks/README.md)
- [服务化部署](/docs/service/README.md)
    - [API调用](/docs/service/flask.md)
    - [交互式前端](/docs/service/chainlit.md)
    - [公有云部署](/docs/service/cloud.md)
- [二次开发](/docs/develop_guide/README.md)


## 开源社区与活动
<div align="center">
<h3>百度智能云千帆AppBuilder-SDK微信交流群</h3>
<img src='docs/image/wechat_group.png' alt='wechat' width='200' >
</div>

- [Github Issue](https://github.com/baidubce/app-builder/issues):  提交安装/使用问题、报告bug、建议新特性、沟通开发计划等

- [百度智能云千帆社区](https://cloud.baidu.com/qianfandev)：
    - [千帆杯新手训练营 - 多类型主题练习赛](https://cloud.baidu.com/qianfandev/aimatch)
    - [千帆杯AI原生应用创意挑战赛 - 教育生态行业赛](https://cloud.baidu.com/qianfandev/topic/269711)
    - [千帆杯AI原生应用创意挑战赛 - 效率工具常规赛](https://cloud.baidu.com/qianfandev/topic/269599)



## License

AppBuilder-SDK遵循Apache-2.0开源协议。

