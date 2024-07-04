# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from importlib import import_module

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

from appbuilder.utils.trace._function import _post_trace, _client_run_trace, _client_tool_trace
from appbuilder import logger

_MODULE_1 = 'appbuilder'
_MODULE_2 = 'appbuilder-sdk-ext'


class AppbuilderInstrumentor(BaseInstrumentor):
    """
    Instrumentor for appbuilder and appbuilder-sdk-ext.
    """

    __slots__ = (
        "_original_session_post",
        '_original_client_run',
        '_original_client_tool',
    )
    def instrumentation_dependencies(self):
        pass

    def _instrument(self, **kwargs):
        if not (tracer_provider := kwargs.get("tracer_provider")):
            tracer_provider = trace.get_tracer_provider()

        tracer = trace.get_tracer(
            instrumenting_module_name=__name__,
            tracer_provider=tracer_provider,
        )

        # 保存原始函数的引用

        try:
            from .tracer_wrapper import  session_post_func, client_run_trace_func, client_tool_trace_func
            self._original_session_post = session_post_func
            self._original_client_run = client_run_trace_func
            self._original_client_tool =  client_tool_trace_func
        except:
            raise ImportError(
                "Please check if the run_trace, tool_eval_streaming_trace, and assistant_trace methods are missing from the file.")

        # 保证trace对appbuilder与appbuilder-sdk-ext的兼容性
        try:
            appbuilder = import_module(_MODULE_1)
        except:
            appbuilder = None

        try:
            appbuilder_sdk_ext = import_module(_MODULE_2)
        except:
            appbuilder_sdk_ext = None
        
        def _appbuilder_session_post(wrapped, instance, args, kwargs):
            return _post_trace(tracer, self._original_session_post, *args, **kwargs)
        
        def _appbuilder_client_run_trace(wrapped, instance, args, kwargs):
            return _client_run_trace(tracer, self._original_client_run, *args, **kwargs)
        
        def _appbuilder_client_tool_trace(wrapped, instance, args, kwargs):
            return _client_tool_trace(tracer, self._original_client_tool, *args, **kwargs)
        
        # 引用相关函数并替换
        if appbuilder:
            
            wrap_function_wrapper(
                module = _MODULE_1,
                name='utils.trace.tracer_wrapper.session_post_func',
                wrapper=_appbuilder_session_post
            )

            wrap_function_wrapper(
                module = _MODULE_1,
                name = 'utils.trace.tracer_wrapper.client_run_trace_func',
                wrapper= _appbuilder_client_run_trace
            )

            wrap_function_wrapper(
                module = _MODULE_1,
                name = 'utils.trace.tracer_wrapper.client_tool_trace_func',
                wrapper = _appbuilder_client_tool_trace
            )

        if not appbuilder_sdk_ext and not appbuilder:
            raise Exception("appbuilder and appbuilder-sdk-ext not found")

    def _uninstrument(self):
        # 恢复原始函数
        try:
            from appbuilder.utils.trace.tracer_wrapper import session_post_func, client_run_trace_func, client_tool_trace_func
            session_post_func = self._original_session_post
            client_run_trace_func = self._original_client_run
            client_tool_trace_func = self._original_client_tool
        except:
            print("appbuilder not found")
            

def create_tracer_provider(enable_phoenix: bool = True, enable_console: bool = False, host: str = "127.0.0.1", port: int = 8080, method: str = "/v1/traces"):
    tracer_provider = TracerProvider()

    if enable_phoenix:  # 将trace数据在本地可视化界面展示
        endpoint = f"{host}:{port}{method}"
        logger.info("OTLPSpanExporter endpoint: {}".format(endpoint))
        tracer_provider.add_span_processor(
            SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

    if enable_console:  # 将trace数据在控制台展示
        tracer_provider.add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter()))

    return tracer_provider


class AppBuilderTracer():
    def __init__(self, enable_phoenix: bool = True, enable_console: bool = False, host: str = "http://localhost", port: int = 8080, method="/v1/traces") -> None:
        self._tracer_provider = create_tracer_provider(
            enable_phoenix=enable_phoenix,
            enable_console=enable_console,
            host=host,
            port=port,
            method=method
        )
        self._instrumentor = AppbuilderInstrumentor()

    @property
    def tracer_provider(self):
        return self._tracer_provider
    
    @property
    def instrumentor(self):
        return self._instrumentor

    def add_custom_processor(self, processor):
        self._tracer_provider.add_span_processor(processor)

    def start_trace(self):
        logger.info("AppBuilder Starting trace...")
        self._instrumentor._instrument(tracer_provider=self._tracer_provider)

    def end_trace(self):
        logger.info("AppBuilder Ending trace...")
        self._instrumentor._uninstrument()

    def __enter__(self):
        self.start_trace()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_trace()
