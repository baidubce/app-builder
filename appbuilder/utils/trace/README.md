# Appbuilder-SDK TRACE 

## 使用方法

### ①将Appbuilder-sdk的Trace信息输出到控制台

此功能可以将跟踪到的Appbuilder-SDK组件运行信息以span形式输出到控制台

#### 设置环境变量

```python
# 设置环境变量
os.environ["APPBUILDER_SDK_TRACER_CONSOLE"] = "true"
```

#### 加载tracer_provider并为Appbuilder-SDK打桩

```python
# 加载tracer_provider
from appbuilder import create_tracer_provider, AppbuilderInstrumentor
tracer_provider = create_tracer_provider()

# 启动AppbuilderInstrumentor打桩器
instrumentor=AppbuilderInstrumentor()
instrumentor.instrument(tracer_provider=tracer_provider)
```

#### 运行你的Apppbuilder-SDK组件

```python
# 运行你的appbuilder组件,运行过程中会自动实现跟踪
# 此代码仅为示例代码，组件运行代码查看组件对应Cookbook
play = appbuilder.Playground()
play.run()
```

**输出结果：**
```
{
    "name": "run(CompletionBaseComponent)",
    "context": {
        "trace_id": "0xe2afaf9e3be5881c0c9605e6b33ce037",
        "span_id": "0x92c7285732b36fb9",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": "0x72446a5399ad91b4",
    "start_time": "2024-06-19T06:37:21.608246Z",
    "end_time": "2024-06-19T06:37:29.067811Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "time.cost-time": "7.459135055541992s",
        "openinference.span.kind": "LLM",
        "input.id": "00e9c77b-78d3-424a-b043-134f9b11c667",
        "input.Message-name": "msg",
        "input.Message-type": "str",
        "input.value.message": "Message(name=msg, content=\u4f60\u597d\uff0c\u5c0f\u660e\uff0c\u6211\u662f\u673a\u5668\u4eba\uff0c\u673a\u5668\u4eba\u662f\u4e00\u4e2a\u804a\u5929\u673a\u5668\u4eba\uff0c\u6211\u53ef\u4ee5\u804a\u5929\uff0c\u4f60\u53ef\u4ee5\u95ee\u6211\u4f60\u597d\u5417\uff1f\u3002, mtype=str)",
        "tips": "\u6ce8\u610f:\u82e5\u8f93\u5165\u4e3a\u9ed8\u8ba4\u503c\uff0c\u5219\u4e0d\u8bb0\u5f55",
        "output.id": "e6d9f94a-d26f-4af6-bfec-75448efdc483",
        "output.Message-name": "msg",
        "output.Message-type": "dict",
        "output.value": "\u4f60\u597d\u5440\uff0c\u5c0f\u660e\uff01\u6211\u662f\u673a\u5668\u4eba\uff0c\u5f88\u9ad8\u5174\u548c\u4f60\u804a\u5929\u3002\u4f60\u6709\u4ec0\u4e48\u95ee\u9898\u6216\u8005\u60f3\u804a\u4ec0\u4e48\u90fd\u53ef\u4ee5\u544a\u8bc9\u6211\u54e6\uff01\u4f60\u95ee\u6211\u201c\u4f60\u597d\u5417\uff1f\u201d\uff0c\u6211\u5f53\u7136\u5f88\u597d\u5566\uff0c\u8c22\u8c22\u5173\u5fc3\uff01\u4f60\u5462\uff0c\u6709\u4ec0\u4e48\u65b0\u9c9c\u4e8b\u60f3\u5206\u4eab\uff0c\u6216\u8005\u6709\u4ec0\u4e48\u95ee\u9898\u60f3\u8981\u95ee\u6211\u5417\uff1f\u6211\u4f1a\u5c3d\u6211\u6240\u80fd\u6765\u56de\u5e94\u4f60\u3002",
        "output.extra": "{}",
        "llm.token_count.prompt": 22,
        "llm.token_count.completion": 58,
        "llm.token_count.total": 80
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.25.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
```

#### 恢复打桩器

```python
instrumentor.uninstrument()
```

### ②将Appbuilder-sdk的Trace信息发送到本地软件并可视化展示

#### 准备阶段

##### 安装与启动phoenix软件

- 建议独立使用独立的python环境启动Phoenix，也可将Phoenix部署到远程服务器上，此处以本地启动为例
- 若未安装phoenix，请启动trace包中的phoenix.sh脚本文件安装phoenix
- 使用独立的py文件运行tracer_launch启动器，以防阻塞
- 使用ctrl+c结束phoenix程序运行

```python
from appbuilder import tracer_launch

# 不添加参数，启动Phoenix，并无结束时间
tracer_launch()

# 添加参数，启动Phoenix，结束时间为1小时
tracer_launch(worktime=3600)

```

**启动后，在浏览器中打开http://127.0.0.1:6006/接口，即可访问并查看,使用Ctrl+C结束Phoenix运行**

#### 设置环境变量

```python
# 设置环境变量
os.environ["APPBUILDER_SDK_TRACER_PHOENIX"] = "true"
```

#### 加载tracer_provider并为Appbuilder-SDK打桩

```python
# 加载tracer_provider
from appbuilder import create_tracer_provider, AppbuilderInstrumentor
tracer_provider = create_tracer_provider()

# 启动AppbuilderInstrumentor打桩器
instrumentor=AppbuilderInstrumentor()
instrumentor.instrument(tracer_provider=tracer_provider)
```

#### 运行你的Apppbuilder-SDK组件

```python
# 运行你的appbuilder组件,运行过程中会自动实现跟踪
# 此代码仅为示例代码，组件运行代码查看组件对应Cookbook
play = appbuilder.Playground()
play.run()
```

#### 恢复打桩器

```python
instrumentor.uninstrument()
```

- 点击phoenix可视化界面地址，即可访问并查看跟踪结果界面，地址默认为本地http://127.0.0.1:6006/接口.


### ③将Appbuilder-sdk的Trace信息储存在本地

#### 创建本地储存容器

```python
from appbuilder import LocalSpanExporter
locals = LocalSpanExporter()
```

#### 向tracer_provider添加本地储存器并为Appbuilder-SDK打桩

```python
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# 向tracer_provider添加本地储存器
tracer_provider = create_tracer_provider()
tracer_provider.add_span_processor(SimpleSpanProcessor(locals))

# 启动AppbuilderInstrumentor打桩器
instrumentor=AppbuilderInstrumentor()
instrumentor.instrument(tracer_provider=tracer_provider)
```

#### 运行你的Apppbuilder-SDK组件

```python
# 运行你的appbuilder组件,运行过程中会自动实现跟踪
# 此代码仅为示例代码，组件运行代码查看组件对应Cookbook
play = appbuilder.Playground()
play.run()
```

#### 恢复打桩器

```python
instrumentor.uninstrument()
```

### ④Appbuilder-SDK Trace使用拓展

可以自行选择传输方式，tracer_provider 内的传输方式决定了跟踪信息发送方式，下述代码就是三种信息传输方式同步运行的代码展示(同时进行①②③三种传输方式)

```python
# 同时设置多个环境变量
os.environ["APPBUILDER_SDK_TRACER_PHOENIX"] = "true"
os.environ["APPBUILDER_SDK_TRACER_CONSOLE"] = "true"

# 加载tracer_provider
from appbuilder import create_tracer_provider, AppbuilderInstrumentor
tracer_provider = create_tracer_provider()

# 创建本地储存器
from appbuilder import LocalSpanExporter
locals = LocalSpanExporter()

# 向tracer_provider添加本地储存器
tracer_provider.add_span_processor(SimpleSpanProcessor(locals))
```

**注意：开发者也可以创建自己的tracer_provider,并传入打桩器，实现自定义信息传输方式**
