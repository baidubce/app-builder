# Appbuilder-SDK TRACE 

## 使用方法

### 启动Phoenix可视化软件

**注意:没有可视化需求的可忽略此步骤**

**如果未安装phoenix，需要先安装phoenix软件(这里提供清华园下载方式)** 

```bash
python3 -m pip install arize-phoenix==4.5.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**启动phoenix服务**

```bash
appbuilder_trace_server
```

- 使用ctrl+c停止phoenix服务

### 启动Appbuilder-SDK TRACE

```python
from appbuilder import AppBuilderTracer
tracer=AppBuilderTracer(
    enable_phoenix = True,
    enable_console = False,
    )
```

- enable_phoenix:是否启动phoenix可视化跟踪
- enable_console:是否将trace信息反馈到控制台

```python
# 启动trace 
import os
import appbuilder

tracer.start_trace()

os.environ["APPBUILDER_TOKEN"] = "YOUR_APPBUILDER_TOKEN"
app_id = "YOUR_APP_ID"

builder = appbuilder.AppBuilderClient(app_id)
conversation_id = builder.create_conversation()
msg = builder.run(conversation_id=conversation_id, query="你可以做什么？",stream=True)

for m in msg.content:
    print(m)

# 结束trace
tracer.end_trace()
```

- Phoenix可视化效果

![Phoenix可视化效果](https://bj.bcebos.com/v1/appbuilder-sdk-components/Phoenix%E5%8F%AF%E8%A7%86%E5%8C%96%E7%95%8C%E9%9D%A2%EF%BC%883%EF%BC%89.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-07-03T03%3A19%3A12Z%2F-1%2Fhost%2Fe79bcd6c9edbae95c98d789464621986fbb74b2f5a10936a555a1fe89f435624)