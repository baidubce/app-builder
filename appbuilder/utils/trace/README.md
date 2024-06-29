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
# 设置 timeout 为 10 秒
python3 phoenix_wrapper.py --timeout 10

# 不设置 timeout，服务常驻运行
python3 phoenix_wrapper.py

phoenix_wrapper.py文件路径为:appbuilder/utils/trace/phoenix_wrapper.py
```

### 启动Appbuilder-SDK TRACE

```python
from appbuilder.utils.trace.tracer import AppBuilderTracer
tracer=AppBuilderTracer(
    enable_phoenix = True,
    enable_console = False,
    )
```

- enable_phoenix:是否启动phoenix可视化跟踪
- enable_console:是否将trace信息反馈到控制台

```python
# 启动trace 
tracer.start_trace()

os.environ["APPBUILDER_TOKEN"] = "YOUR_APPBUILDER_TOKEN"
app_id = "YOUR_APPBUILDER_ID"

builder = appbuilder.AppBuilderClient(app_id)
conversation_id = builder.create_conversation()
msg = builder.run(conversation_id=conversation_id, query="你可以做什么？",stream=True)

for m in msg.content:
    print(m)

# 结束trace
tracer.end_trace()
```

**接下来你就可以在Phoenix和控制台中查看你的trace信息了**