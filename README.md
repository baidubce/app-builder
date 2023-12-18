<div align="center">

<h1>AppBuilder-SDK</h1>

AppBuilder SDK面向开发者提供AI原生应用一站式开发工具，包括基础云资源、AI能力引擎、千帆大模型以及相关能力组件，提升AI原生应用开发效率。

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/baidubce/app-builder/app-builder.svg)](https://github.com/baidubce/app-builder/releases)
![Supported Python versions](https://img.shields.io/badge/python-3.8+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)

</div>

## 教程与文档

* **预备步骤**
  * [认证鉴权](./docs/authentication.md)
  * [组件总览](./docs/components.md)
* **API文档**
  * [API Docs](./docs/api_reference/)


## 快速安装

执行如下命令，快速安装Python语言的最新版本AppBuilder-SDK（要求Python >= 3.8)。

```shell
pip install --upgrade appbuilder-sdk
```

## 快速使用

使用AppBuilder SDK之前，请首先申请并设置鉴权参数。具体请参考[认证鉴权](./docs/authentication.md)。

``` python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "Bearer bce-YOURTOKEN"
```

### 典型示例

AppBuilder包括基于大模型构建AI原生应用的各类范式，包括基于Prompt模版的文本生成、检索增强的生成、使用外部工具的文本生成等。

#### 空模版(Playground)
```python
import appbuilder

# 空模版组件
template_str = "你扮演{role}, 请回答我的问题。\n\n问题：{question}。\n\n回答："
playground = appbuilder.Playground(prompt_template=template_str, model="ernie-bot-4")

# 定义输入，调用空模版组件
input = appbuilder.Message({"role": "java工程师", "question": "java语言的内存回收机制是什么"})
print(playground(input, stream=False, temperature=0.0))

```

#### 文本生成(Text Completion)
```python
import appbuilder

# 相似问生成组件
similar_q = appbuilder.SimilarQuestion(model="eb-turbo-appbuilder")

# 定义输入，调用相似问生成
input = appbuilder.Message("我想吃冰淇淋，哪里的冰淇淋比较好吃？")
print(similar_q(input))

```

#### 对话式问答(Chat RAG)
```python
空
```

#### AI能力引擎(AI Engine)
```python
import appbuilder

# 语音识别组件
asr = appbuilder.ASR()
asr_path = './appbuilder/tests/asr_test.pcm'

# 从文件读取pcm文件，调用asr组件识别结果
with open(asr_path, "rb") as f:
    inp = appbuilder.Message(content={"raw_audio": f.read()})
    asr_out = asr(inp)
    print(out.content)

```

## 应用服务化

AppBuilder-SDK提供对组件的服务化能力。通过定义Agent，开发者可以快速启动Chainlit、Flask等服务化的Demo或API提供快速体验环境。

```python
import os
import sys
import appbuilder

# 空模版组件
playground = appbuilder.Playground(
    prompt_template="{query}",
    model="ernie-bot-4"
)

# 使用AgentBase来服务化playground组件
agent = appbuilder.AgentBase(component=component)

# 启动chainlit demo，会自动在浏览器打开体验对话框页面
agent.chainlit_demo(port=8091)
```

## License

AppBuilder-SDK遵循Apache-2.0开源协议。
