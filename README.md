<div align="center">

<h1>AppBuilder-SDK</h1>

AppBuilder SDK面向开发者提供AI原生应用一站式开发工具，包括基础云资源、AI能力引擎、千帆大模型以及相关能力组件，提升AI原生应用开发效率。

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.8+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)

</div>

## News
* **[云端快速创建RAG、Agent、GBI等应用](https://console.bce.baidu.com/ai_apaas/app)**
* **[官方组件列表](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#%E5%BC%80%E5%8F%91%E7%BB%84%E4%BB%B6)**
* **v0.1.0版本发布**：[Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.1.0)
  * 2023.12.19初始版本发布，基础云组件支持包括BES；AI能力引擎语音、视觉类10个能力，大模型相关RAG、文本生成能力19个。
* **v0.2.0版本发布** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.2.0)
  * 2023.01.03发布，核心升级点GBI相关组件新增，v0.1.0遗留问题修复
* **v0.3.0版本发布**
  * 新增组件：新增了百度搜索rag组件（RAGwithBaiduSearch)。[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/rag_with_baidusearch.ipynb)
  * AgentRuntime更新：1) AgentBase 更名为 AgentRuntime，并增强了数据管理能力。2) AgentRuntime添加了对LLMMessage.extra字段的支持，增加了create_flask_app用于WSGI服务器运行服务，修复了UserSession重复初始化的问题。[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/agent_runtime.ipynb)
  * 模型列表获取：与千帆大模型平台模型名打通，可动态获取当前账号模型名，并在组件中使用[获取模型列表](https://github.com/baidubce/app-builder/blob/master/README.md#%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8)
  * 可通过官方镜像开发和运行实例代码[二次开发](https://github.com/baidubce/app-builder/blob/master/README.md#%E4%BA%8C%E6%AC%A1%E5%BC%80%E5%8F%91)
* **v0.4.0版本发布**
  * AppBuilder Console SDK发布[知识集合Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/console_dataset.ipynb)，[RAG调用Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/console_rag.ipynb)
  * 大模型组件新增：Excel2Figure(基于Excel信息画图表)
  * AI能力引擎组件新增&更新：植物识别、动物识别、表格文字识别V2、手写文字识别、二维码识别、身份证混贴识别、文档矫正识别、图像内容理解、流式TTS
  * AgentRuntime：新增[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/agent_runtime.ipynb)
* **v0.4.1版本发布**
  * 支持以下功能进行FunctionCall调用：动植物识别、表格文字识别、条形码及二维码识别、身份证混贴识别、手写文字识别、text2image、excel2figure

## 教程与文档

* **预备步骤**
  * [认证鉴权](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6)
  * [开通组件权限](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#2%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1)
* **API文档**
  * [API Docs](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz)


## 快速安装

执行如下命令，快速安装Python语言的最新版本AppBuilder-SDK（要求Python >= 3.8)。

```shell
pip install --upgrade appbuilder-sdk
```
如果在本地无法跑通appbuilder-sdk包，也可以使用我们的官方镜像来按照和运行，具体方案参考**二次开发**部分。

## 快速使用

使用AppBuilder SDK之前，请首先申请并设置鉴权参数。具体请参考[认证鉴权](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6)。

``` python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

## 模型列表

AppBuilder提供获取千帆模型列表的函数，在运行具体组件之前，可以先获取当前账号下可以使用的模型列表，代码如下：
``` python
import appbuilder
import os

os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
models = appbuilder.get_model_list(api_type_filter=["chat"], is_available=True)
print(", ".join(models))
```

填写自己的Token，获取模型列表输出如下：
``` shell
ERNIE-Bot 4.0, ERNIE-Bot-8K, ERNIE-Bot, ERNIE-Bot-turbo, EB-turbo-AppBuilder专用版, Qianfan-Chinese-Llama-2-7B, Yi-34B-Chat, Llama-2-7B-Chat, Llama-2-13B-Chat, Llama-2-70B-Chat, ChatGLM2-6B-32K, ChatLaw, BLOOMZ-7B, Qianfan-BLOOMZ-7B-compressed, AquilaChat-7B
```

为方便用户更容易使用模型，以下是一些模型的短名称
| 千帆模型名                   | AppBuilder-SDK短名 |
|----------------------------|------------------|
| ERNIE-Bot 4.0              |       eb-4       |
| ERNIE-Bot-8K               |       eb-8k      |
| ERNIE-Bot                  |       eb         |
| ERNIE-Bot-turbo            |       eb-turbo   |
| ERNIE Speed-AppBuilder   |       ernie_speed_appbuilder           |


### 典型示例

AppBuilder包括基于大模型构建AI原生应用的各类范式，包括基于Prompt模版的文本生成、检索增强的生成、使用外部工具的文本生成等。

#### 空模版(Playground)
```python
import appbuilder

# 空模版组件
template_str = "你扮演{role}, 请回答我的问题。\n\n问题：{question}。\n\n回答："
playground = appbuilder.Playground(prompt_template=template_str, model="ERNIE Speed-AppBuilder")

# 定义输入，调用空模版组件
input = appbuilder.Message({"role": "java工程师", "question": "java语言的内存回收机制是什么"})
print(playground(input, stream=False, temperature=1e-10))

```

#### 文本生成(Text Completion)
```python
import appbuilder

# 相似问生成组件
similar_q = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

# 定义输入，调用相似问生成
input = appbuilder.Message("我想吃冰淇淋，哪里的冰淇淋比较好吃？")
print(similar_q(input))

```

#### 检索增强问答(Chat RAG)
```python
import appbuilder
import os

# 此处APPBUILDER_TOKEN为限制QPS的试用账号，请在测试您自己的应用时替换为自己的账号Token
os.environ["APPBUILDER_TOKEN"] = ""

# 此处填写线上RAG应用ID，可在【AppBuilder网页端-我的应用界面】查看
# 网页链接 https://console.bce.baidu.com/ai_apaas/app
app_id = ""
rag_app = appbuilder.console.RAG(app_id)
query = "中国的首都在哪里"
answer = rag_app.run(appbuilder.Message(query)) # 新建对话
print(answer.content)
```

## 应用服务化

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
    model="ERNIE Speed-AppBuilder"
)

# 使用 AgentRuntime 来服务化playground组件
agent = appbuilder.AgentRuntime(component=playground)

# 启动chainlit demo，会自动在浏览器打开体验对话框页面
agent.chainlit_demo(port=8091)
```

## 二次开发
当前面向开发者提供开放的数据结构，包括Message和Component，方便开发者融入个人已有的大模型应用程序。此部分仍在不断建设中。
二次开发可以采用官方提供的开发镜像，便于快速安装各种依赖库。
``` shell
docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.1.0
```

### 消息(Message)
- 构建大模型应用的统一数据结构，基于Pydantic构建，在不同的Component之间流动。Message基类的默认字段是content，类型是Any。
```python
from appbuilder import Message
input_dict = Message({"query": "红烧肉怎么做"})
input_list = Message(["text1", "text2", "text3"])
input_str = Message("红烧肉怎么做")
```

### 组件(Component)
- 所有能力单元的标准结构，以Message结构作为输入输出，内部执行逻辑可在本地执行或调用云端服务，以下是官方组件的实现示例。
```python
class SimilarQuestionMeta(ComponentArguments):
    """ SimilarQuestionMeta
    """
    message: Message = Field(..., 
                             variable_name="query", 
                             description="输入消息，用于模型的输入，一般为问题。")


class SimilarQuestion(CompletionBaseComponent):
    """ 基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
    Examples:

        .. code-block:: python
            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = "..."

            qa_mining = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

            msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
            msg = appbuilder.Message(msg)
            answer = qa_mining(msg)

            print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    def __init__(self, model=None):
        """初始化SimilarQuestionMeta任务。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
        
        Returns:
            None
        
        """
        super().__init__(SimilarQuestionMeta, model=model)

    def run(self, message, stream=False, temperature=1e-10):
        """
        给定输入（message）到模型运行，同时指定运行参数，并返回结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature)
```

## License

AppBuilder-SDK遵循Apache-2.0开源协议。
