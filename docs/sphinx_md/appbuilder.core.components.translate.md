# appbuilder.core.components.translate package

## Submodules

## appbuilder.core.components.translate.component module

文本翻译-通用版组件

### *class* appbuilder.core.components.translate.component.Translation(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文本翻译组件,可支持中、英、日、韩等200+语言互译，100+语种自动检测。
支持语种列表可参照 [https://ai.baidu.com/ai-doc/MT/4kqryjku9#%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8](https://ai.baidu.com/ai-doc/MT/4kqryjku9#%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8)

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

translate = appbuilder.Translation()
resp = translate(appbuilder.Message("你好\n中国"), to_lang="en")
# 输出 {'from_lang':'zh', 'to_lang':'en', 'trans_result':[{'src':'你好','dst':'hello'},{'src':'中国','dst':'China'}]}
print(resp.content)
```

#### manifests *= [{'description': '文本翻译通用版工具，会根据指定的目标语言对文本进行翻译，并返回翻译后的文本。', 'name': 'translation', 'parameters': {'properties': {'q': {'description': '需要翻译的源文本，文本翻译工具会将该文本翻译成对应的目标语言', 'type': 'string'}, 'to_lang': {'description': "翻译的目标语言类型，'en'表示翻译成英语, 'zh'表示翻译成中文，'yue'表示翻译成粤语，'wyw'表示翻译成文言文，'jp'表示翻译成日语，'kor'表示翻译成韩语，'fra'表示翻译成法语，'spa'表示翻译成西班牙语，'th'表示翻译成泰语,'ara'表示翻译成阿拉伯语，'ru'表示翻译成俄语，'pt'表示翻译成葡萄牙语，'de'表示翻译成德语，'it'表示翻译成意大利语，'el'表示翻译成希腊语，'nl'表示翻译成荷兰语,'pl'表示翻译成波兰语,'bul'表示翻译成保加利亚语，'est'表示翻译成爱沙尼亚语，'dan'表示翻译成丹麦语, 'fin'表示翻译成芬兰语，'cs'表示翻译成捷克语，'rom'表示翻译成罗马尼亚语，'slo'表示翻译成斯洛文尼亚语，'swe'表示翻译成瑞典语，'hu'表示翻译成匈牙利语，'cht'表示翻译成繁体中文，'vie'表示翻译成越南语，默认为'en'", 'enum': ['en', 'zh', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it', 'el', 'nl', 'pl', 'bul', 'est', 'dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie'], 'type': 'string'}}, 'required': ['q'], 'type': 'object'}}]*

#### name *= 'translate'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), from_lang: str = 'auto', to_lang: str = 'en', timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

根据提供的文本以及语种参数执行文本翻译

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 翻译文本。
  * **from_lang** (*str*) – 翻译的源语言。默认为 “auto”。
  * **to_lang** (*str*) – 翻译的目标语言。默认为 “en”。
  * **timeout** (*float* *,* *optional*) – 翻译请求的超时时间。
  * **retry** (*int* *,* *optional*) – 重试次数。
* **返回:**
  返回的文本翻译结果。
  例如，Message(content={‘from_lang’: ‘zh’, ‘to_lang’: ‘en’, ‘trans_result’: [{‘src’: ‘你好’, ‘dst’: ‘hello’}]})
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

工具函数，用于翻译指定的文本。

* **参数:**
  * **name** (*str*) – 函数名称，此参数在本函数中未使用。
  * **streaming** (*bool*) – 是否流式输出翻译结果。
  * **\*\*kwargs** – 关键字参数，可以包含以下参数：
    - traceid (str, optional): 请求的唯一标识符，默认为None。
    - q (str): 待翻译的文本。
    - to_lang (str, optional): 目标语言代码，默认为”en”。
* **返回:**
  如果streaming为True，则返回生成器，生成包含翻译结果的字典；
  如果streaming为False，则返回包含翻译结果的JSON字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 如果未设置参数”q”，则抛出此异常。

#### version *= 'v1'*
