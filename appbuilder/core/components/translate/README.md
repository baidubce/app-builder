# 文本翻译-通用版（Translation）

## 简介
文本翻译组件（Translation）提供200+语种互译的在线文本翻译服务。支持术语定制功能，用户可对翻译结果进行干预，快速提高翻译质量。可广泛应用于移动端、PC网站、智能硬件等不同产品形态中，满足多领域、多场景的翻译需求。

## 基本用法
通过如下示例代码可以快速开始使用文本翻译组件：
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

translate = appbuilder.Translation()
resp = translate(appbuilder.Message("你好\n中国"), from_lang="zh", to_lang="en")
# 输出{'from_lang': 'zh', 'to_lang': 'en', 'trans_result': [{'src': '你好', 'dst': 'hello'}, {'src': '中国', 'dst': 'China'}]}
print(resp.content)
```
其中，`APPBUILDER_TOKEN`为您的API访问授权token。

## 参数说明
### 初始化参数说明
Translation组件无需额外初始化参数。

### 调用参数说明
`run`函数的参数定义如下：
- `message`：需要翻译的文本，为Message类型，必传参数。
- `from_lang`：翻译的源语言，默认为`auto`，表示自动检测语言。
- `to_lang`：需要翻译的目标语言，默认为`en`，表示英语。
- `timeout`：请求翻译的超时时间，非必传参数，默认为None。
- `retry`：请求失败的重试次数，非必传参数，默认为0。

返回值为Message类型的对象，包含翻译后的文本。
例如，`Message(content={'from_lang': 'zh', 'to_lang': 'en', 'trans_result': [{'src': '你好', 'dst': 'hello'}]})`