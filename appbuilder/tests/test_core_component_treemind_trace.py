import appbuilder
from appbuilder import TreeMind, Message
from appbuilder import AppBuilderTracer

tracer=AppBuilderTracer(
    enable_phoenix = True,
    enable_console = False,
)

tracer.start_trace()
tm = TreeMind()
msg = Message(content = "生成一份年度总结的思维导图")
result = tm.run(msg)
print(result)
tracer.end_trace()