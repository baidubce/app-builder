# 文本翻译-通用版（Translation）

## 简介
文本翻译组件（Translation）提供200+语种互译的在线文本翻译服务。支持术语定制功能，用户可对翻译结果进行干预，快速提高翻译质量。可广泛应用于移动端、PC网站、智能硬件等不同产品形态中，满足多领域、多场景的翻译需求。

### 功能介绍
支持200+语种互译，传入待翻译内容，并指定源语言（支持语种自动检测）和目标语言，即可获得翻译结果，并支持术语干预

### 特色优势
1. 依托互联网数据资源和自然语言处理技术优势，上线全球首个互联网神经网络翻译系统，日均响应千亿字符请求
2. 2019国际机器翻译评测（WMT19）中，获得中英翻译第一，提供业界领先的机器翻译服务
3. 支持用户上传术语对翻译结果进行干预，优化翻译质量，用户可根据不同产品、不同领域创建多个术语库
4. 翻译请求可实现实时响应，服务稳定性高，在海外也可及时获取翻译结果，保障用户稳定的服务体验

### 应用场景
1. 教育学习：在外语教学及学习场景中，通过实时句子翻译、单词释义、语音合成等功能，帮助师生沟通、外教课后点评，辅助阅读和写作，全面提升学习效率与质量
2. 手机厂商：应用于手机系统中，实现手机系统取词翻译、对话文本翻译等服务。为手机应用开发者提供便捷的翻译功能
3. 跨境电商：在商业全球化背景下，针对跨国商贸服务中产品名称、详情页等网站基本信息进行翻译，助力企业开拓国际市场
4. 智能硬件：应用于翻译机、学习机、智能手表等硬件系统中，为用户提供文本翻译、词典及语音合成等能力，实现便捷准确的多语种互译功能

## 基本用法
通过如下示例代码可以快速开始使用文本翻译组件：
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

translate = appbuilder.Translation()
resp = translate(appbuilder.Message("你好\n中国"), from_lang="zh", to_lang="en")
# 输出{'from_lang': 'zh', 'to_lang': 'en', 'trans_result': [{'src': '你好', 'dst': 'hello'}, {'src': '中国', 'dst': 'China'}]}
print(resp.content)
```

## 参数说明
### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数说明
无

### 调用参数说明
|参数名称 |参数类型 |是否必须 |描述 | 示例值    |
|--------|--------|--------|----|--------|
|message |String  |是 |输入的请求翻译文本| Message("你好") |
|from_lang|String|否 |翻译的源语言，默认为`auto`，表示自动检测语言。| zh    |
|to_lang|Integer|否 |需要翻译的目标语言，默认为`en`，表示英语。| en  |
|timeout|Integer|是 |HTTP超时时间| 10     |
|retry|Integer|是 |HTTP重试次数| 3      |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|from_lang  |String  |翻译源语言| zh|
|to_lang  |String  |翻译目标语言|en|
|trans_result  |List[Object]  |返回结果|[{'src': '你好', 'dst': 'hello'}]|
|trans_result.src  |String  |源文本|你好|
|trans_result.dst  |String  |目标文本|hello|

### 响应示例
```json
{"from_lang": "zh", "to_lang": "en", "trans_result": [{"src": "你好", "dst": "hello"}]}
```