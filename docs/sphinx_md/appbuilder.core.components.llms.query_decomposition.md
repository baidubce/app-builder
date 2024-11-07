# appbuilder.core.components.llms.query_decomposition package

## Submodules

## appbuilder.core.components.llms.query_decomposition.component module

query decomposition

### *class* appbuilder.core.components.llms.query_decomposition.component.QueryDecomposition(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

尝试对已经判定为复杂问题的原始问题进行拆解，把复杂问题拆解为一个个简单问题。广泛用于知识问答场景。

Examples:

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

query_decomposition = appbuilder.QueryDecomposition(model="Qianfan-Agent-Speed-8k")

msg = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
msg = appbuilder.Message(msg)
answer = query_decomposition(msg)

print("Answer: \n{}".format(answer.content))
```

#### meta

`QueryDecompositionMeta` 的别名

#### name *: str* *= 'query_decomposition'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*
