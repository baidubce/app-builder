# 多轮改写 (QueryRewrite)

## 简介
多轮改写组件 (QueryRewrite) 是一个用于处理多轮对话和查询改写的组件。它主要用于理解和优化用户与机器人的交互过程，进行指代消解及省略补全。该组件支持不同的改写类型，可根据对话历史生成更准确的用户查询。

### 功能介绍
多轮改写组件 (QueryRewrite) 据用户和机器人的聊天记录，改写用户当前query，利用大语言模型的理解及生成能力，进行指代消解及省略补全。

### 特色优势
多轮改写组件 (QueryRewrite) ，基于百度自研的大语言模型文心一言，无需更多的prompt描述，即可根据对话历史生成更准确的用户查询。

### 应用场景
多轮改写组件 (QueryRewrite) 可用于智能问答、对话式搜索等场景。

## 基本用法

以下是一个简单的例子，展示如何快速开始使用 QueryRewrite 组件：

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

# 初始化并使用 QueryRewrite 组件
query_rewrite = appbuilder.QueryRewrite(model="ERNIE Speed-AppBuilder")
answer = query_rewrite(appbuilder.Message(['我应该怎么办理护照？', '您可以查询官网或人工咨询', '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']), rewrite_type="带机器人回复")
print(answer)
```

## 参数说明

### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数
|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
|message |Message  |是 |需要改写的文本，用于模型的主要输入内容，这是一个必需的参数。 |Message(content=['我应该怎么办理护照？', '您可以查询官网或人工咨询','我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']) |
|rewrite_type |str |否 |改写类型选项，可选值为 '带机器人回复'(改写时参考user查询历史和assistant回复历史)，'仅用户查询'(改写时参考user查询历史)。 默认是"带机器人回复" |"带机器人回复" |
|stream |bool | 否 |指定是否以流式形式返回响应。默认为 False。 |False |
|temperature |float | 否 |模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。对于此组件勿动！ |1e-10 |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |Message  |返回结果|Message(content="身份证在哪办")|

### 响应示例
```
Message(name=msg, content="身份证在哪办", mtype=dict, extra={})
```

## 示例和案例研究
实际应用中，QueryRewrite 可用于多种场景，如信息检索、智能对话等。

## 更新记录和贡献
当前版本：v2 (2023-12)
