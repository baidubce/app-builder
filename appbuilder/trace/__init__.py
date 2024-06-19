import os
import logging
from importlib import import_module
from typing import Collection 

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor 
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SimpleSpanProcessor,
    ConsoleSpanExporter
) 
from wrapt import wrap_function_wrapper


from .package import _instruments 
from ._function import _run_trace,_assistant_trace,_tool_eval_streaming_trace 

from ._tracer import run_trace, tool_eval_streaming_trace, assistant_trace 
from .local_tracer import launch_tracer

__all__ = (
    "AppbuilderInstrumentor",
    "LocalSpanExporter",
    "run_trace",
    "tool_eval_streaming_trace",
    "assistant_trace",
    "launch_tracer"
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


_MODULE_1 = 'appbuilder'
_MODULE_2 = 'appbuilder-sdk-ext'


class LocalSpanExporter(SpanExporter):
    def __init__(self):
        self.spans = []

    def export(self, span_data):
        for span in span_data:
            self.spans.append(span.to_json())


class AppbuilderInstrumentor(BaseInstrumentor):
    """
    Instrumentor for appbuilder and appbuilder-sdk-ext.
    """

    __slots__ = (
            "_origin_run",
            "_original_tool",
            "_original_assistant",
        )
    

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self,**kwargs):
        

        if not (tracer_provider := kwargs.get("tracer_provider")):
            tracer_provider = trace.get_tracer_provider()

        tracer=trace.get_tracer(
            instrumenting_module_name=__name__,
            tracer_provider=tracer_provider,
        )

        # 保存原始函数的引用
        
        try:
            from ._tracer import run_trace_func, tool_eval_streaming_trace_func, assistant_trace_func 
            self._origin_run = run_trace_func
            self._origin_tool = tool_eval_streaming_trace_func
            self._origin_assistant = assistant_trace_func
        except:
            raise ImportError("Please check if the run_trace, tool_eval_streaming_trace, and assistant_trace methods are missing from the file.")
        
        
        # 保证trace对appbuilder与appbuilder-sdk-ext的兼容性
        try:
            appbuilder = import_module(_MODULE_1)
        except:
            appbuilder = None

        try:
            appbuilder_sdk_ext = import_module(_MODULE_2)
        except:
            appbuilder_sdk_ext = None
        
        def _appbuilder_run_trace(wrapped,instance,args,kwargs):
            return _run_trace(tracer, self._origin_run, *args, **kwargs)
        
        def _appbuilder_tool_eval_streaming_trace(wrapped,instance,args,kwargs):
            return _tool_eval_streaming_trace(tracer, self._origin_tool, *args, **kwargs)
        
        def _appbuilder_assistant_trace(wrapped,instance,args,kwargs):
            return _assistant_trace(tracer, self._origin_assistant, *args, **kwargs)
        
        def _apppbuilder_sdk_ext_run_trace(wrapped,instance,args,kwargs):
            return _run_trace(tracer, self._origin_run,*args, **kwargs)
        
        def _apppbuilder_sdk_ext_tool_eval_streaming_trace(wrapped,instance,args,kwargs):
            return _tool_eval_streaming_trace(tracer, self._origin_tool, *args, **kwargs)

        # 引用相关函数并替换
        if appbuilder:
            wrap_function_wrapper(
                module = _MODULE_1,
                name = 'trace._tracer.run_trace_func',
                wrapper = _appbuilder_run_trace
            )

            wrap_function_wrapper(
                module = _MODULE_1,
                name = 'trace._tracer.tool_eval_streaming_trace_func',
                wrapper = _appbuilder_tool_eval_streaming_trace
            )

            wrap_function_wrapper(
                module = _MODULE_1,
                name = 'trace._tracer.assistant_trace_func',
                wrapper = _appbuilder_assistant_trace
            )
        
        if appbuilder_sdk_ext:
            wrap_function_wrapper(
                module = _MODULE_2,
                name = 'trace._tracer.run_trace_func',
                wrapper = _apppbuilder_sdk_ext_run_trace
            )

            wrap_function_wrapper(
                module = _MODULE_2,
                name = 'trace._tracer.tool_eval_streaming_trace_func',
                wrapper = _apppbuilder_sdk_ext_tool_eval_streaming_trace
            )
        
        if not appbuilder_sdk_ext and not appbuilder:
            raise Exception("appbuilder and appbuilder-sdk-ext not found")
        
    def _uninstrument(self):
        # 恢复原始函数
        try:
            from appbuilder.trace._tracer import run_trace_func, tool_eval_streaming_trace_func, assistant_trace_func 
            run_trace_func = self._origin_run
            tool_eval_streaming_trace_func = self._origin_tool
            assistant_trace_func = self._origin_assistant
        except:
            print("appbuilder not found")
        
        try:
            from appbuilder_sdk_ext.trace._tracer import run_trace_func, tool_eval_streaming_trace_func 
            run_trace_func = self._origin_run
            tool_eval_streaming_trace_func = self._origin_tool

        except:
            print("appbuilder-sdk-ext not found,If you are an appbuilder user, please disregard this feedback.")


def create_tracer_provider():
    tracer_provider = TracerProvider()
    
    if os.getenv('APPBUILDER_SDK_TRACER_PHOENIX', 'false').lower() == 'true': # 将trace数据在本地可视化界面展示
        endpoint = "http://127.0.0.1:6006/v1/traces"
        tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))
    
    if os.getenv('APPBUILDER_SDK_TRACER_CONSOLE', 'false').lower() == 'true': # 将trace数据在控制台展示
        tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    
    return tracer_provider