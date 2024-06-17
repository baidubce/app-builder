# 口语化Query生成（Oral Query Generation）

## 简介
口语化Query生成组件（Oral Query Generation）可以基于输入文本生成与文档内容相关的Query。

### 功能介绍
基于输入文本生成与文档内容相关的Query。

### 特色优势
生成的query划分为问题和短语两种类型，可分别用于不同场景。

### 应用场景
可用于推荐问题生成、标签生成、文档索引增强等。

## 基本用法
### 快速开始
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."


text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
        '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
        '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
        '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
        '，实时视频分享您的生活。')

#! 该组件推荐使用ERNIE Speed-AppBuilder模型。
oral_query_generation = appbuilder.OralQueryGeneration(model='ERNIE Speed-AppBuilder')
result = oral_query_generation(appbuilder.Message(text), query_type='全部', output_format='str')

print(result)
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `model` | str | 是 | 模型名称，用于指定要使用的千帆模型。推荐使用ERNIE Speed-AppBuilder模型。 | ERNIE Speed-AppBuilder |
| `secret_key` | str | 否 | 用户鉴权token，默认从环境变量中获取: `os.getenv("APPBUILDER_TOKEN", "")` | bce-v3/XXX |
| `gateway` | str | 否 | 后端网关服务地址，默认从环境变量中获取: `os.getenv("GATEWAY_URL", "")` | https://appbuilder.baidu.com |
| `lazy_certification` | bool | 否 | 延迟认证，为True时在第一次运行时认证。默认为False。 | False |

### 调用参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `message` | obj | 是 | 输入消息，用于模型的主要输入内容。 | Message(content='...') |
| `query_type` | str | 否 | 待生成的query类型，包括问题、短语和全部（问题+短语）。默认为全部。 | 全部 |
| `output_format` | str | 否 | 输出格式，包括json和str。默认为str。 | str |
| `stream` | bool | 否 | 指定是否以流式形式返回响应。默认为 False。 | False |
| `temperature` | float | 否 | 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。 | 0.1 |
| `top_p` | float | 否 | 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0.0。 | 0.0 |

### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- |
| `result` | obj | 模型运行后的输出结果 | Message(content='...') |

### 响应示例
```
Message(name=msg, content=1. OPPO Reno5上有什么特殊的功能？
2. 视频超级防抖是什么？
3. 视频超级防抖有什么作用？
4. 如何在OPPO Reno5上开启视频超级防抖？
5. 视频超级防抖Pro是什么？
6. 开启视频超级防抖后，屏幕上会出现什么？
7. 前置视频有防抖算法吗？
8. OPPO Reno5上的视频超级防抖
9. 视频超级防抖3.0
10. 多代视频防抖算法积累的作用
11. 开启视频超级防抖的方法
12. 视频超级防抖Pro的功能
13. 开启视频超级防抖后，屏幕上会出现的东西
14. 前置视频防抖算法的作用, mtype=dict, extra={})
```

## 高级用法

## 更新记录和贡献
### 2024.5.22
#### [Updated]
- 升级能力，主要升级内容如下：
  - 生成的query要求能够使用输入文本进行回答。
  - 生成的query划分为问题和短语类型。
  - 生成的query数量不再限制为10个。
- 在调用组件时，支持输出问题、短语或全部（问题 + 短语）；支持输出格式为json或者str（兼容之前版本的输出格式）。

### 2024.1.24
#### [Updated]
- 更新README。

### 2023.12.07
#### [Added]
- 增加口语化Query生成组件。
- 增加口语化Query生成组件单元测试。