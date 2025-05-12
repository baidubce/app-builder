<div align="center">
<img src='docs/image/logo.png' alt='logo' width='700' >
<br>

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.9+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)
</div>

简体中文 | [English](./docs/README_en.md) | [日本語](./docs/README_ja.md)

<br>

## 🚀 欢迎使用 AppBuilder-SDK

AppBuilder-SDK 是百度智能云千帆AppBuilder面向AI原生应用开发者提供的一站式开发平台客户端SDK。无论你是AI新手还是资深开发者，都能在这里找到适合你的AI应用开发方案。

### ✨ 为什么选择 AppBuilder-SDK？

| 特性 | 描述 | 优势 |
|------|------|------|
| 丰富的AI能力 | 40+个百度生态优质组件 | 开箱即用，无需重复开发 |
| 灵活的部署方式 | 支持本地、云端、API等多种部署 | 适应不同场景需求 |
| 完整的开发工具 | 提供监控、调试、追踪等工具 | 提升开发效率 |
| 活跃的社区支持 | 微信交流群、Github社区 | 快速解决问题 |

### 🎯 我能用 AppBuilder-SDK 做什么？

#### 1. 构建智能应用
- **RAG应用**：构建基于知识库的智能问答系统，支持文档解析、切片、向量化、检索等完整流程
- **Agent应用**：开发具有自主决策能力的AI助手，支持工具调用、多轮对话、状态管理
- **工作流应用**：通过可视化编排或代码方式构建复杂的AI处理流程

#### 2. 调用AI能力
- **大模型调用**：支持多种大模型，可自定义prompt
- **组件调用**：40+个百度生态优质组件
- **MCP组件**：支持将本地组件转换为MCP服务

#### 3. 部署与监控
- **多种部署方式**：支持Flask、Chainlit、公有云部署
- **完整的监控工具**：提供可视化Tracing、DebugLog等

### 🛠️ 快速开始

#### 1. 环境要求
- Python >= 3.9
- 使用MCP组件功能需要 Python >= 3.12
- 支持的操作系统：Linux、Windows、MacOS

#### 2. 安装SDK
```bash
python3 -m pip install --upgrade appbuilder-sdk
```

#### 3. 选择你的开发路径

<div align="center">
<img src='docs/image/quickstart-flow.png' alt='quickstart-flow' width='600' >
</div>

| 开发路径 | 适合人群 | 推荐文档 |
|---------|---------|---------|
| 新手入门 | 刚接触AI开发 | [快速开始指南](./docs/QuickStart/StartFirstAINativeApplication/README.md) |
| 组件开发 | 想开发自定义组件 | [MCP组件开发指南](./cookbooks/mcp/server.ipynb) |
| 应用开发 | 已有AI开发经验 | [应用开发指南](./docs/Application/README.md) |

### 📚 学习资源

#### 1. 基础教程
- [组件使用示例](./cookbooks/components/README.md)
- [工作流编排指南](./cookbooks/pipeline/README.md)
- [端到端应用示例](./cookbooks/end2end_application/README.md)

#### 2. 进阶教程
- [MCP组件开发](./cookbooks/mcp/README.md)
- [公有云部署](./cookbooks/advanced_application/cloud_deploy.ipynb)
- [性能优化指南](./docs/DevelopGuide/AdvancedDevelopment/README.md)

### 🔥 最新特性：MCP组件支持

AppBuilder-SDK 最新版本支持将本地组件转换为MCP服务，实现端云组件联动。主要特性包括：

| 特性 | 描述 | 文档链接 |
|------|------|---------|
| 组件服务化 | 将本地组件转换为MCP服务 | [MCP组件开发指南](./cookbooks/mcp/server.ipynb) |
| 端云联动 | 实现本地组件与云端组件的联动 | [端云组件联动示例](./cookbooks/end2end_application/agent/tool_call.ipynb) |

### 💡 快速示例

#### 1. 调用大模型
```python
import appbuilder
import os

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = "your-token-here"

# 定义prompt模板
template_str = "你扮演{role}, 请回答我的问题。\n\n问题：{question}。\n\n回答："

# 定义输入，调用playground组件
input = appbuilder.Message({"role": "java工程师", "question": "请简要回答java语言的内存回收机制是什么，要求100字以内"})

playground = appbuilder.Playground(prompt_template=template_str, model="Qianfan-Agent-Speed-8K")

# 以打字机的方式，流式展示大模型回答内容
output = playground(input, stream=True, temperature=1e-10)
for stream_message in output.content:
    print(stream_message)
```

#### 2. 调用能力组件
```python
import appbuilder
import os

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = "your-token-here"

# 创建组件实例
rag_with_baidu_search_pro = appbuilder.RagWithBaiduSearchPro(model="ERNIE-3.5-8K")

# 执行组件
input = appbuilder.Message("9.11和9.8哪个大")
result = rag_with_baidu_search_pro.run(
    message=input,
    instruction=appbuilder.Message("你是专业知识助手"))

# 输出运行结果
print(result.model_dump_json(indent=4))
```

#### 3. 使用MCP组件
```python
import os
from appbuilder.mcp_server.server import MCPComponentServer
from appbuilder.core.components.v2 import Translation, Text2Image

os.environ['APPBUILDER_TOKEN'] = 'your-token-here'

# 定义server
server = MCPComponentServer(name="AB Component Server")

# 初始化组件实例
translation = Translation()
text2image = Text2Image()

# 把组件作为tool添加到server
server.add_component(translation)
server.add_component(text2image)

# 启动server
server.run()
```

### 🤝 加入社区

<div align="center">
<h3>加入我们的微信交流群</h3>
<img src='docs/image/wechat_group.png' alt='wechat' width='200' >
</div>

- [Github Issue](https://github.com/baidubce/app-builder/issues): 提交问题、报告bug、建议新特性
- [百度智能云千帆社区](https://cloud.baidu.com/qianfandev): 参与社区活动、获取最新资讯

### 📄 文档导航

- [完整文档目录](./docs/README.md)
- [API参考](./docs/API/README.md)
- [更新日志](./docs/DevelopGuide/ChangeLog/changelog.md)
- [常见问题](./docs/DevelopGuide/ErrorMessage/error_message.md)

## License

AppBuilder-SDK遵循Apache-2.0开源协议。 