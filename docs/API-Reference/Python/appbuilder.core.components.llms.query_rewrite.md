# appbuilder.core.components.llms.query_rewrite package

## Submodules

## appbuilder.core.components.llms.query_rewrite.component module

多轮改写

### *class* appbuilder.core.components.llms.query_rewrite.component.QueryRewrite(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

多轮改写大模型组件， 基于生成式大模型进行多轮对话query改写的组件。它主要用于理解和优化用户与机器人的交互过程，进行指代消解及省略补全。该组件支持不同的改写类型，可根据对话历史生成更准确的用户查询。

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

query_rewrite = appbuilder.QueryRewrite(model="ERNIE Speed-AppBuilder")
answer = query_rewrite(appbuilder.Message(['我应该怎么办理护照？',
                                            '您可以查询官网或人工咨询',
                                            '我需要准备哪些材料？',
                                            '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》',
                                            '在哪里办']),
                                            rewrite_type="带机器人回复")
```

#### meta

`QueryRewriteArgs` 的别名

#### name *: str* *= 'query_rewrite'*

#### run(message, rewrite_type='带机器人回复', stream=False, temperature=1e-10, top_p=0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) -- Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **rewrite_type** (*str* *,*  *可选*) -- 改写类型选项，可选值为 '带机器人回复'(改写时参考user查询历史和assistant回复历史)，
    '仅用户查询'(改写时参考user查询历史)。默认为"带机器人回复"。
  * **stream** (*bool* *,*  *可选*) -- 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) -- 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) -- 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj
* **抛出:**
  **ValueError** -- 如果输入消息为空或不符合要求，将抛出 ValueError 异常。

#### version *: str* *= 'v1'*
