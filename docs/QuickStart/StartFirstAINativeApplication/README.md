# 快速开始

该文档目录包含以下内容：

- [SDK安装](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/StartFirstAINativeApplication/install.md)
- [版本更新历史](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/ChangeLog/changelog.md)

## 预备步骤
在正式开始使用AppBuilder-SDK之前，可以阅读以下内容：

* **预备步骤**
  * [认证鉴权](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6)
  * [开通组件权限](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#2%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1)
* **API文档**
  * [API Docs](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz)

## 快速上手


### 获取模型列表

AppBuilder提供获取千帆模型列表的函数，在运行具体组件之前，可以先获取当前账号下可以使用的模型列表，代码如下：
``` python
import appbuilder
import os

# 设置环境中的TOKEN，请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "your api key"
models = appbuilder.get_model_list(api_type_filter=["chat"], is_available=True)
print(", ".join(models))
```

填写自己的Token，获取模型列表输出示例如下：
``` shell
ERNIE-Bot 4.0, ERNIE-Bot, ERNIE-3.5-8K-0205, ERNIE-Speed, DeepSeek-V3.1, ERNIE-Character-8K, EB-turbo-AppBuilder专用版, ChatLaw, ERNIE-Bot-8K
```

为方便用户更容易使用模型，以下是一些模型的短名称
| 千帆模型名                   | AppBuilder-SDK短名 |
|----------------------------|------------------------------|
| ERNIE-Bot 4.0              |       eb-4                   |
| ERNIE-Bot                  |       eb                     |
| ERNIE-Bot-turbo            |       eb-turbo               |
| EB-turbo-AppBuilder专用版   |      ernie_speed_appbuilder  |
| DeepSeek-V3.1              |      deepseek-v3.1-250821    |



### 空模版(Playground)
```python
import appbuilder
import os

# 设置环境中的TOKEN，请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "your api key"

# 空模版组件
template_str = "你扮演{role}, 请回答我的问题。\n\n问题：{question}。\n\n回答："
playground = appbuilder.Playground(prompt_template=template_str, model="DeepSeek-V3.1")

# 定义输入，调用空模版组件
input = appbuilder.Message({"role": "java工程师", "question": "java语言的内存回收机制是什么"})
print(playground(input, stream=False, temperature=1e-10))

```

### 文本生成(Text Completion)
```python
import appbuilder
import os

# 设置环境中的TOKEN，请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "your api key"

# 相似问生成组件
similar_q = appbuilder.SimilarQuestion(model="DeepSeek-V3.1")

# 定义输入，调用相似问生成
input = appbuilder.Message("我想吃冰淇淋，哪里的冰淇淋比较好吃？")
print(similar_q(input))

```

### 检索增强问答
```python
import appbuilder
import os

# 设置环境中的TOKEN，请替换为您的个人TOKEN
os.environ["APPBUILDER_TOKEN"] = "your api key"

# 此处填写线上Agent应用ID，可在【AppBuilder网页端-我的应用界面】查看
# 本示例提供的Agent应用为：地理小达人
# 网页已部署的应用链接为「地理小达人」：https://appbuilder.baidu.com/s/x1tSF
# 以下示例代码展示了如何代码态调用并集成到您的应用中的能力
app_id = "42eb211a-14b9-43d2-9fae-193c8760ef26"
builder = appbuilder.AppBuilderClient(app_id)
conversation_id = builder.create_conversation()

answer = builder.run(conversation_id, "中国的首都在哪里")
print(answer.content)
```

### 应用服务化

AppBuilder-SDK提供对组件的服务化能力。通过定义Agent，开发者可以快速启动Chainlit、Flask等服务化的Demo或API提供快速体验环境。

在需要部署服务的环境中，开发者需要首先手动安装 Chainlit 库

```shell
pip install chainlit
```
而后，使用AppBuilder的Agent服务化功能，即可快速部署服务

```python
import appbuilder

# 空模版组件
playground = appbuilder.Playground(
    prompt_template="{query}",
    model="DeepSeek-V3.1"
)

# 使用 AgentRuntime 来服务化playground组件
agent = appbuilder.AgentRuntime(component=playground)

# 启动chainlit demo，会自动在浏览器打开体验对话框页面
agent.chainlit_demo(port=8091)
```

也可以对AppBuilderClient进行服务化，快速部署

```python
import os
from appbuilder.core.component import Component
from appbuilder import (
    AgentRuntime,
    AppBuilderClient,
)


if __name__ == "__main__":
    # 设置环境中的TOKEN，请替换为您的个人TOKEN
    os.environ["APPBUILDER_TOKEN"] = "your api key"

    # 此处填写线上Agent应用ID，可在【AppBuilder网页端-我的应用界面】查看
    # 本示例提供的Agent应用为：地理小达人
    # 网页已部署的应用链接为「地理小达人」：https://appbuilder.baidu.com/s/x1tSF
    app_id = "42eb211a-14b9-43d2-9fae-193c8760ef26"
    agent_builder = AppBuilderClient(app_id)
    agent = AgentRuntime(component=agent_builder)
    agent.chainlit_agent(port=8091)
```