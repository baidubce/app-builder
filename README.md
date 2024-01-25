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
  * 新增组件：新增了百度搜索rag组件（RAGwithBaiduSearch）和其他组件。
  * AgentRuntime更新：1) AgentBase 更名为 AgentRuntime，并增强了数据管理能力。2) AgentRuntime添加了对LLMMessage.extra字段的支持，增加了create_flask_app用于WSGI服务器运行服务，修复了UserSession重复初始化的问题。
  * 模型列表获取：与千帆大模型平台模型名打通，可动态获取当前账号模型名，并在组件中使用
  * 可通过官方镜像开发和运行实例代码

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

### 典型示例

AppBuilder包括基于大模型构建AI原生应用的各类范式，包括基于Prompt模版的文本生成、检索增强的生成、使用外部工具的文本生成等。

#### 空模版(Playground)
```python
import appbuilder

# 空模版组件
template_str = "你扮演{role}, 请回答我的问题。\n\n问题：{question}。\n\n回答："
playground = appbuilder.Playground(prompt_template=template_str, model="eb-4")

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

#### 检索增强问答(Chat RAG)
```python
import appbuilder
from pathlib import Path

cluster_id = "your_bes_cluster_id"
username = "your_bes_cluster_username"
password = "your_bes_cluster_password"

# 基于doc_parser和doc_splitter解析file_path文件为若干个段落
def parse_file(file_path, doc_parser, doc_splitter):
    input_msg = appbuilder.Message(str(file_path))
    doc_parser_result = doc_parser(input_msg, return_raw=True)
    doc_splitter_result = doc_splitter(doc_parser_result)
    return [f"{file_path.name}+{para['text'][:384]}" 
            for para in doc_splitter_result.content["paragraphs"]]

# 文档切分的分块大小，每个分块最大340个字符
chunk_size = 340
# 声明文档解析和文档切分组件
doc_parser = appbuilder.DocParser()
doc_splitter = appbuilder.DocSplitter(splitter_type="split_by_chunk", max_segment_length=chunk_size)       

file_dir = "./files"
# 批量解析，形成段落切片列表
paragraphs = [para_text for file in Path(file_dir).iterdir() if file.is_file()
            for para_text in parse_file(file, doc_parser, doc_splitter)]

# 默认使用erniebot-embedding-v1
embedding = appbuilder.Embedding()

# 将段落切片列表入库到BESVectorStoreIndex，这里面用到的Baidu Elastic Search服务
segments = appbuilder.Message(resume_paragraphs)
vector_index = appbuilder.BESVectorStoreIndex.from_segments(
    segments=segments, cluster_id=cluster_id, user_name=username, 
    password=password, embedding=embedding)

# 在线检索部分
retriever = vector_index.as_retriever()

input_msg = appbuilder.Message("appbuilder是什么？")
result_list = retriever(query=input_msg, top_k=3)
context_msg = appbuilder.Message([item["text"] for item in result_list])

mrc = appbuilder.MRC()
rag_result = mrc(input_msg, context_msg)

print(rag_result.content)

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
    print(asr_out.content)
```

## 应用服务化

AppBuilder-SDK提供对组件的服务化能力。通过定义Agent，开发者可以快速启动Chainlit、Flask等服务化的Demo或API提供快速体验环境。

```python
import appbuilder

# 空模版组件
playground = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
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

            qa_mining = appbuilder.SimilarQuestion(model="eb-turbo-appbuilder")

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
