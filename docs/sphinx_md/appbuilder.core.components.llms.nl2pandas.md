# appbuilder.core.components.llms.nl2pandas package

## Submodules

## appbuilder.core.components.llms.nl2pandas.component module

### *class* appbuilder.core.components.llms.nl2pandas.component.Nl2pandasComponent(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

自然语言转pandas大模型组件， 基于生成式大模型对query进行理解并生成对应语义的可执行python代码（主要使用pandas），可用于基于表格的查询、问答等多种场景。

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
table_info = '''表格列信息如下：
学校名 : 清华附小 , 字符串类型，代表小学学校的名称
所属地区 : 西城区 , 字符串类型，表示该小学学校所在的位置
创办时间 : 1998 , 数字值类型，表示该小学学校的创办时间
类别 : 公立小学 , 字符串类型，表示该小学学校所在的类别
学生人数 : 2000 , 数字值类型，表示该小学学校的学生数量
教职工人数 : 140 , 数字值类型，表示该小学学校的教职工数量
教学班数量 : 122 , 数字值类型，表示该小学学校的教学班数量
'''
query = "海淀区有哪些学校"
query = appbuilder.Message(query)

nl2pandas = appbuilder.Nl2pandasComponent(model="Qianfan-Agent-Speed-8k")
answer = nl2pandas(query, table_info = table_info)
```

#### meta

`Nl2pandasArgs` 的别名

#### name *: str* *= 'nl2pandas'*

#### run(message, table_info=None, stream=False, temperature=1e-10, top_p=0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*table_info*) – Message): 输入问题，通常是针对表格信息的提问，如’海淀区的小学有哪些’。这是一个必需的参数。
  * **(****obj** – Message, optional): 表格信息，包括表格列名、对应列名的示例和释义。默认值为 None，但这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*
