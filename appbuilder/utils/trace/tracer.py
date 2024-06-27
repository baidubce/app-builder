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

from appbuilder.utils.trace._function import _run_trace, _assistant_trace, _tool_eval_streaming_trace
from appbuilder.utils.trace.tracer_wrapper import run_trace, tool_eval_streaming_trace, assistant_trace
from appbuilder.utils.trace.phoenix_wrapper import tracer_launch
from appbuilder import logger

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

    def _instrument(self, **kwargs):
        if not (tracer_provider := kwargs.get("tracer_provider")):
            tracer_provider = trace.get_tracer_provider()

        tracer = trace.get_tracer(
            instrumenting_module_name=__name__,
            tracer_provider=tracer_provider,
        )

        # 保存原始函数的引用

        try:
            from .tracer_wrapper import run_trace_func, tool_eval_streaming_trace_func, assistant_trace_func
            self._origin_run = run_trace_func
            self._origin_tool = tool_eval_streaming_trace_func
            self._origin_assistant = assistant_trace_func
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

        def _appbuilder_run_trace(wrapped, instance, args, kwargs):
            return _run_trace(tracer, self._origin_run, *args, **kwargs)

        def _appbuilder_tool_eval_streaming_trace(wrapped, instance, args, kwargs):
            return _tool_eval_streaming_trace(tracer, self._origin_tool, *args, **kwargs)

        def _appbuilder_assistant_trace(wrapped, instance, args, kwargs):
            return _assistant_trace(tracer, self._origin_assistant, *args, **kwargs)

        def _apppbuilder_sdk_ext_run_trace(wrapped, instance, args, kwargs):
            return _run_trace(tracer, self._origin_run, *args, **kwargs)

        def _apppbuilder_sdk_ext_tool_eval_streaming_trace(wrapped, instance, args, kwargs):
            return _tool_eval_streaming_trace(tracer, self._origin_tool, *args, **kwargs)

        # 引用相关函数并替换
        if appbuilder:
            wrap_function_wrapper(
                module=_MODULE_1,
                name='trace._tracer.run_trace_func',
                wrapper=_appbuilder_run_trace
            )

            wrap_function_wrapper(
                module=_MODULE_1,
                name='trace._tracer.tool_eval_streaming_trace_func',
                wrapper=_appbuilder_tool_eval_streaming_trace
            )

            wrap_function_wrapper(
                module=_MODULE_1,
                name='trace._tracer.assistant_trace_func',
                wrapper=_appbuilder_assistant_trace
            )

        if appbuilder_sdk_ext:
            wrap_function_wrapper(
                module=_MODULE_2,
                name='trace._tracer.run_trace_func',
                wrapper=_apppbuilder_sdk_ext_run_trace
            )

            wrap_function_wrapper(
                module=_MODULE_2,
                name='trace._tracer.tool_eval_streaming_trace_func',
                wrapper=_apppbuilder_sdk_ext_tool_eval_streaming_trace
            )

        if not appbuilder_sdk_ext and not appbuilder:
            raise Exception("appbuilder and appbuilder-sdk-ext not found")

    def _uninstrument(self):
        # 恢复原始函数
        try:
            from appbuilder.utils.trace.tracer_wrapper import run_trace_func, tool_eval_streaming_trace_func, assistant_trace_func
            run_trace_func = self._origin_run
            tool_eval_streaming_trace_func = self._origin_tool
            assistant_trace_func = self._origin_assistant
        except:
            print("appbuilder not found")

        try:
            from appbuilder.utils.trace.tracer_wrapper import run_trace_func, tool_eval_streaming_trace_func
            run_trace_func = self._origin_run
            tool_eval_streaming_trace_func = self._origin_tool

        except:
            pass


def create_tracer_provider(enable_phoenix: bool = True, enable_console: bool = False, host: str = "127.0.0.1", port: int = 8080, method: str = "/v1/traces"):
    tracer_provider = TracerProvider()

    if enable_phoenix:  # 将trace数据在本地可视化界面展示
        endpoint = f"{host}:{port}{method}"
        tracer_provider.add_span_processor(
            SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

    if enable_console:  # 将trace数据在控制台展示
        tracer_provider.add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter()))

    return tracer_provider


class AppBuilderTracer():
    def __init__(self, enable_phoenix: bool = True, enable_console: bool = False, host: str = "127.0.0.1", port: int = 8080, method="/v1/traces") -> None:
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
