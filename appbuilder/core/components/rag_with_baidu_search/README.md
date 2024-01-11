# RAG With BaiduSearch

## 简介
RAG with BaiduSearch是基于生成式大模型的问答组件，使用百度搜索引擎检索候选文本进行检索增强。

## 基本用法

### 快速开启

```python
import appbuilder
import os
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建rag_with_baidusearch对象
rag_with_baidusearch_component = appbuilder.RAGWithBaiduSearch(model="eb-turbo-appbuilder")

# 初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)

# 模拟运行rag_with_baidusearch基本组件
result = rag_with_baidusearch_component.run(msg)

# 获取reference
references = result.extra

# 输出运行结果
print(result)
```




## 参数说明

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数

- `msg (obj:Message)`: 输入消息，包含用户提出的问题。这是一个必需的参数。
- `instruction (obj:Message, 可选)`: 可设定人设，如：你是问答助手，在回答问题前需要加上“很高兴为您解答：”
- `reject (bool, 可选)`: 拒绝开关，如果为 True，则启用该能力。默认为 False。当输入的问题在搜索结果中没有找到答案时，开关开启时，模型会用特定话术("当前文档库找不到对应的答案，我可以尝试用我的常识来回答你。")做回复的开头，并后接自有知识做回复内容。
- `clarify (bool, 可选)`: 澄清开关，如果为 True，则启用该能力。默认为 False。 当输入的问题比较模糊、或者主体指代不清晰，且context_list中包含有可以回答该模糊问题的多种潜在备选答案时，开启该开关，大模型会以特定的话术做澄清反问，引导用户继续补充问题发问。举例子，query:发电机的续航时间？ Answer: 根据搜索结果得到了xx和xx两种型号的发电机，您的问题具体涉及到哪一个？请补充关键信息，作为完整的问题重新发问。
- `highlight (bool, 可选)`: 重点强调开关，如果为 True，则启用该能力。默认为 False。开启该功能时，回复结果中会高亮显示关键部分的内容。
- `friendly (bool, 可选)`: 友好性提升开关，如果为 True，则启用该能力。默认为 False。开关开启时，部分回复的开头会加礼貌用语。且如果回答涉及到大段的信息，会倾向于以<总-分>或者<总-分-总>的形式做分点论述，使得答案的格式更规整，可读性更强。
- `cite (bool, 可选)`: 溯源开关，如果为 True，则启用该能力。默认为 False。开关开启时，回复内容后会使用引用标记来标注回答内容参考的搜索结果序号，如^[1]^ (引用单个搜索结果）,^[1][2]^（引用多个搜索结果）。例如：按照当地公安机关出入境管理部门规定的其他材料办理^[2]^。
- `stream (bool, 可选)`: 指定是否以流式形式返回响应。默认为 False。
- `temperature (float, 可选)`: 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
- `top_p (float, 可选)`: 模型配置的top_p参数，top_p值越高输出文本越多样，top_p值越低输出文本越稳定。取值范围为 0.0 到 1.0，默认值为 1e-10。
- 
### 返回值
- 返回一个 `Message` 对象，包含模型运行后的输出消息。


## 高级用法
该组件的高级用法包括定制化的输入处理、输出处理，以及更复杂的调用场景。用户可以根据具体需求扩展组件功能，实现个性化的问答系统。
包括如下功能：
1、拒答
2、澄清反问
3、重点强调
4、友好度提升
5、溯源
6、人设


### 代码样例
```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建rag_with_baidusearch对象
rag_with_baidusearch_component = appbuilder.RAGWithBaiduSearch(model="eb-turbo-appbuilder")

# 初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)

# 模拟运行rag_with_baidusearch组件，开启拒答、澄清追问、重点强调、友好性提升、溯源能力、人设六个功能
instruction = "你是问答助手，在回答问题前需要加上“很高兴为您解答："
instruction = appbuilder.Message(instruction)
result = rag_with_baidusearch_component.run(msg, reject=True, clarify=True, highlight=True,
                                            friendly=True, cite=True, temperature=0.5, stream=False,
                                            instruction=instruction)

# 输出运行结果
print(result)
```
