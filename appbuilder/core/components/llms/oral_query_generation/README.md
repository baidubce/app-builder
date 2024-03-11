# 口语化Query生成（OralQueryGeneration）

## 简介
口语化Query生成组件（OralQueryGeneration）可以基于输入文本生成与文档内容相关的Query。

### 功能介绍
基于输入文本生成与文档内容相关的Query。

### 特色优势
生成高质量Query。

### 应用场景
可用于文档生成推荐问题、文档索引增强等。

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
oral_query_generation = appbuilder.OralQueryGeneration(model='ERNIE Speed-AppBuilder')
result = oral_query_generation(appbuilder.Message(text))
print(result)
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `model` | str | 否 | 模型名称，用于指定要使用的千帆模型。 | ERNIE Speed-AppBuilder |
| `secret_key` | str | 否 | 用户鉴权token，默认从环境变量中获取: `os.getenv("APPBUILDER_TOKEN", "")` |  |
| `gateway` | str | 否 | 后端网关服务地址，默认从环境变量中获取: `os.getenv("GATEWAY_URL", "")` |  |
| `lazy_certification` | bool | 否 | 延迟认证，为True时在第一次运行时认证。默认为False。 | False |

### 调用参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `message` | obj | 是 | 输入消息，用于模型的主要输入内容。 | Message(content='...') |
| `stream` | bool | 否 | 指定是否以流式形式返回响应。默认为 False。 | False |
| `temperature` | float | 否 | 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。 | 0.1 |

### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- |
| `result` | obj | 模型运行后的输出结果 | Message(content='...') |

### 响应示例
```
Message(name=msg, content=1、OPPO Reno5上的超级防抖
2、怎么开启OPPO Reno5的超级防抖
3、OPPO Reno5的超级防抖Pro
4、前置视频上的超级防抖
5、跑步时拍照OPPO Reno5的超级防抖
6、OPPO Reno5的多代视频防抖
7、OPPO Reno5的超级防抖算法
8、OPPO Reno5的超级防抖怎么用
9、OPPO Reno5的超级防抖如何开启
10、OPPO Reno5的超级防抖Pro如何使用, mtype=dict, extra={})
```

## 高级用法

## 更新记录和贡献
### 2023.12.07
#### [Added]
- 增加口语化Query生成能力。
- 增加口语化Query生成单元测试。

### 2024.1.24
#### [Updated]
- 更新README。