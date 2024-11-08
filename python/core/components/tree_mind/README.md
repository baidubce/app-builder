# 树图 (TreeMind)

## 简介
树图（TreeMind）提供智能思维导图制作工具和丰富的模板，支持脑图、逻辑图、树形图、鱼骨图、组织架构图、时间轴、时间线等多种专业格式。

### 功能介绍   
树图（TreeMind）是一款智能思维导图制作工具，它提供了一个用户友好的平台来创建和编辑各种类型的图表。该工具支持多种专业格式，包括脑图、逻辑图、树形图、鱼骨图、组织架构图、时间轴和时间线等，满足不同用户在不同场景下的需求。

### 特色优势
TreeMind提供丰富的模板，支持多种图表格式，用户可以根据个人需求自由编辑和调整图表。

### 应用场景  
年度总结：用户可以利用TreeMind生成年度总结的思维导图，整理和回顾一年的工作成果和经验教训。
项目管理：在项目管理中，TreeMind可以用来规划项目流程、组织架构和时间线，确保项目按计划进行。
教育和学习：教师和学生可以使用TreeMind来创建课程大纲、学习笔记和复习资料，提高学习效率。
商业策划：商业人士可以利用TreeMind来制定商业策略、市场分析和竞争对手分析等。
会议记录：在会议中，TreeMind可以作为记录工具，帮助整理会议要点和行动计划。

## 基本用法

下面是文生图的代码示例: 

```python
import os
import appbuilder
# 设置环境变量和初始化
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

treemind = appbuilder.TreeMind()
query = "生成一份年度总结的思维导图"
msg = appbuilder.Message(query)
out = treemind.run(msg)
print(out.content)
```
{'result': '生成的思维导图：![图片url](https://static.shutu.cn/shutu/static/open6e/2024/05/24/dbd67eddec13f3a6a75857b9c6e06d85.jpeg)思维导图已经为您生成好了，如果您觉得这个思维导图还不够完美，或者您的想法需要更自由地表达，点击编辑按钮，对思维导图变形、变色、变内容、甚至可以添加新的元素，您可以通过这个链接编辑：https://gapi.shutu.cn/ai/edit-mind-url?works_guid=open5ab4af46187ff7c138fcd95de09efe92_bdappbuilder。', 'img_link': 'https://static.shutu.cn/shutu/static/open6e/2024/05/24/dbd67eddec13f3a6a75857b9c6e06d85.jpeg', 'edit_link': 'https://gapi.shutu.cn/ai/edit-mind-url?works_guid=open5ab4af46187ff7c138fcd95de09efe92_bdappbuilder'}


## 参数说明

### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
无

### 调用参数
| 参数名称    | 参数类型    | 是否必须 | 描述                          | 示例值                                            |
|---------|---------|------|-----------------------------|------------------------------------------------|
| message | obj:`Message`  | 是    | 输入的消息，用于生成思维导图，这是一个必需的参数 | Message(content={"query": "生成一张年终总结的思维导图"}) |

### 响应参数

| 参数名称        |参数类型 | 描述   | 示例 ｜
|-------------|--------|------|------|
| resp | obj:`Message` | 组件返回结果 | Message(name=msg, content={'result': '生成的思维导图：xxx。思维导图已经为您生成好了，如果您觉得这个思维导图还不够完美，或者您的想法需要更自由地表达，点击编辑按钮，对思维导图变形、变色、变内容、甚至可以添加新的元素，您可以通过这个链接编辑：xxx。', 'img_link': 'xxx', 'edit_link': 'xxx'}, mtype=dict)  |