# 多轮改写 (QueryRewrite)

## 简介
多轮改写组件 (QueryRewrite) 是一个用于处理多轮对话和查询改写的组件。它主要用于理解和优化用户与机器人的交互过程，进行指代消解及省略补全。该组件支持不同的改写类型，可根据对话历史生成更准确的用户查询。

## 基本用法

以下是一个简单的例子，展示如何快速开始使用 QueryRewrite 组件：

```python
import os
import appbuilder

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 初始化并使用 QueryRewrite 组件
query_rewrite = appbuilder.QueryRewrite(model="ernie-bot-4")
answer = query_rewrite(appbuilder.Message(['我应该怎么办理护照？', '您可以查询官网或人工咨询', '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']), rewrite_type="带机器人回复")
```
print(answer)
## 参数说明

### 初始化参数

model (str|None): 模型名称，用于指定要使用的千帆模型。

## 调用参数

message (Message): 必传参数，需要改写的文本。
rewrite_type (RewriteTypeChoices): 可选参数，改写类型选项，可选值为 '带机器人回复'(改写时参考user查询历史和assistant回复历史)，'仅用户查询'(改写时参考user查询历史)。 默认是"带机器人回复".
stream (bool): 可选参数，默认为 False，指定是否以流式形式返回响应。
temperature (float): 可选参数，默认为 1e-10，模型配置的温度参数。
返回值：Message 对象，为模型运行后的输出消息。

## 示例和案例研究
实际应用中，QueryRewrite 可用于多种场景，如信息检索、智能对话等。

## API文档
更详细的 API 文档将在后续版本中提供。

## 更新记录和贡献
当前版本：v1
