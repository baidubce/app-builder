# 标签抽取（TagExtraction）

## 简介
标签抽取组件（TagExtraction）是一款高效的标签抽取组件，基于生成式大模型，专门用于从文本中提取关键标签。它适用于各种文本分析场景，如内容分类、关键词提取等。

### 功能介绍
标签抽取组件（TagExtraction）专门设计用于从各类文本中高效地提取关键标签。此组件利用先进的生成式大模型，可以准确识别和提取文本中的重要信息，如关键词、短语或主题。它不仅能快速分析大量文本数据，还能精准识别文本的核心内容，支持用户快速了解文本的主要信息和结构

### 特色优势
- 高效准确：基于先进的生成式大模型，提供高效且准确的标签提取功能。
- 适用广泛：能够处理不同类型和格式的文本数据，适用于多种文本分析场景。
- 格式友好：输出格式采用规范化编号输出，后处理时方便快捷。

### 应用场景
标签抽取组件可以广泛应用于多种场景：

- 内容分类：快速为文章或文档分类，提高信息管理和检索效率。
- 关键词提取：从文本中提取关键词，帮助用户快速了解文本主题和内容。
- 数据分析：在大数据分析中，可以用于预处理，提取有价值的信息。
- 搜索引擎优化：帮助网站或博客提取有效标签，改善其在搜索引擎中的可见度。


## 基本用法

要开始使用 `TagExtraction`，首先需要设置环境变量 `APPBUILDER_TOKEN`，然后创建 `TagExtraction` 实例并传递文本消息。

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

tag_extraction = appbuilder.TagExtraction(model="ERNIE Speed-AppBuilder")
result = tag_extraction(appbuilder.Message("从这段文本中抽取关键标签"))
```

这个例子展示了如何实例化 `TagExtraction` 组件并使用一个文本消息进行标签抽取。

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

无

### 调用参数

|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
|message |String  |是 |需要抽取标签的文本|从这段文本中抽取关键标签|
|stream|bool|否 |指定是否以流式形式返回响应，默认为 False。|True|
|temperature|float|否 |模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。|1e-10|

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |Message  |返回结果|对象，包含模型运行后的输出消息。|
### 响应示例
```json
{"result": "1.5G 2.云计算 3.人工智能 4.数字经济 5.数据中心 6.新型基础设施 7.政策优化 8.产业发展 9.国家重视 10.快速增长"}
```

## 高级用法

高级用法可以包括自定义模型参数或使用不同的模型源。例如，可以通过指定不同的 `model` 来使用特定于域的模型进行标签抽取。

```python
tag_extraction = appbuilder.TagExtraction(model="custom-model")
result = tag_extraction(appbuilder.Message("自定义模型抽取的标签"))
```

## 示例和案例研究

在实际应用中，`TagExtraction` 可以用于新闻文章、社交媒体帖子或其他任何文本内容的关键标签提取，帮助内容创建者或营销分析师快速了解主要主题和趋势。


