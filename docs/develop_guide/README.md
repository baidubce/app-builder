# 开发指引

该文档目录包含以下内容：

- [二次开发基本介绍](https://github.com/baidubce/app-builder/blob/master/docs/develop_guide/README.md)
- [AppBuilder SDK 运行环境超参配置说明](https://github.com/baidubce/app-builder/blob/master/docs/develop_guide/env.md)


## 二次开发
当前已集成Python版本AppBuilder-SDK 0.7.1及相关依赖，方便开发者融入个人已有的大模型应用程序。此部分仍在不断建设中。
二次开发可以采用官方提供的开发镜像，便于快速安装各种依赖库。
``` shell
docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.9.0
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