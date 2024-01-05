# 风格转写 (StyleRewrite)

## 简介
风格转写组件（StyleRewrite） 可以基于生成式大模型对文本的风格进行改写。支持多种文本风格，包括营销、客服、直播、激励及教学话术。

## 基本用法

以下是一个简单的例子，展示如何快速开始使用 StyleRewrite 组件：

```python
import os
import appbuilder

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 初始化并使用 StyleRewrite 组件
style_rewrite = appbuilder.StyleRewrite(model="eb-4")
answer = style_rewrite(appbuilder.Message("文心大模型发布新版"), style="激励话术")
```

## 参数说明

### 初始化参数

model (str|None): 模型名称，用于指定要使用的千帆模型。

## 调用参数

message (Message): 必传参数，需要改写的文本。
style (StyleChoices): 可选参数，想要转换的文本风格，默认为"营销话术"，目前支持营销、客服、直播、激励及教学五种话术。
stream (bool): 可选参数，默认为 False，指定是否以流式形式返回响应。
temperature (float): 可选参数，默认为 1e-10，模型配置的温度参数。
返回值：Message 对象，为模型运行后的输出消息。

## 高级用法


## 示例和案例研究
实际应用中，StyleRewrite 可用于多种场景，如自动化客服、教育内容生成、营销文案生成等。

## API文档
更详细的 API 文档将在后续版本中提供。

## 更新记录和贡献
当前版本：v1
