<div align="center">

<h1>AppBuilder-SDK</h1>

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.9+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)

</div>

`AppBuilder-SDK`是[百度千帆AppBuilder](https://appbuilder.cloud.baidu.com/)面向AI原生应用开发者提供的一站式开发工具。

我们提供自底向上的：基础组件、流程编排、端到端应用 三类功能，满足各类型开发场景，助力效率提升，快速开发并部署AI原生应用。

<div align="center">
<h1>AppBuilder-SDK微信交流群</h1>
<img src='docs/image/wechat_group.png' alt='wechat' width='200' >

</div>

##  如何安装

#### AppBuilder-SDK 最新版本 0.7.0 (2024-04-30)

`AppBuilder-SDK` 更新记录&最新特性请查阅我们的[版本说明](./docs/release_note.md)

#### 我们推荐安装Python最新稳定版本

```bash
python3 -m pip install --upgrade appbuilder-sdk
```
#### 我们也支持多种语言及镜像使用

`Java` 及 `Go` 版本安装，以及通过`docker`镜像使用，请查阅[安装说明](./docs/install.md)


## 快速开始你的第一个AI原生应用

- 示例为`python`版本`端到端应用`代码，请在安装`appbuilder-sdk`后使用
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
    - [通用文字识别组件](./cookbooks/general_ocr.ipynb)
    - [基础组件服务化](./cookbooks/agent_runtime.ipynb)
- 流程编排
    - [Assistant SDK](./cookbooks/assistant_function_call.ipynb)
- 端到端应用
    - [Agent应用](./cookbooks/agent_builder.ipynb)
    - [RAG应用](./cookbooks/rag.ipynb)
    - [企业级问答系统](./cookbooks/qa_system_1_dataset.ipynb)


## 系统架构


## 文档


## 开源社区与活动



## License

AppBuilder-SDK遵循Apache-2.0开源协议。

