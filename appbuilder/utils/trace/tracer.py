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

from appbuilder.utils.trace._function import( 
    _post_trace, 
    _client_run_trace, 
    _client_tool_trace, 
    _assistant_tool_trace, 
    _assistant_run_trace,
    _assistant_stream_trace,
    _assistant_stream_run_with_handler_trace,
    _components_run_trace_with_opentelemetry,
    _components_run_trace_with_sentry,
    _components_stream_run_trace_with_opentelemetry,
    _components_stream_run_trace_with_sentry,
    _list_trace,
    )
from appbuilder import logger

_MODULE_1 = 'appbuilder'
_MODULE_2 = 'appbuilder-sdk-ext'


class AppbuilderInstrumentor(BaseInstrumentor):
    """
    Instrumentor for appbuilder and appbuilder-sdk-ext.
    """

    _instance = None
    _instrumented = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    __slots__ = (
        "_original_session_post",
        '_original_client_run',
        '_original_client_tool',
        '_original_assistant_tool',
        '_original_assistant_run',
        '_original_assistant_stream_run',
        '_original_assistant_stream_run_with_handler',
        '_orignal_components_run',
        '_original_components_stream_run',
        '_original_list',
    )
    def instrumentation_dependencies(self):
        pass

    def _instrument(self, **kwargs):
        """
        为指定模块的函数添加跟踪功能。
        
        Args:
            **kwargs: 可选参数，用于提供跟踪器提供程序。
        
        Returns:
            None
        
        Raises:
            ImportError: 如果从文件中缺少`run_trace`、`tool_eval_streaming_trace`和`assistant_trace`方法，则引发此异常。
            Exception: 如果未找到`appbuilder`和`appbuilder-sdk-ext`模块，则引发此异常。
        
        """
        if self._instrumented:
            return
        self._instrumented = True
        
        # 判断是否启用Sentry跟踪，如果启用，则创建虚拟的的Tracer,仅对Components组件生效
        if os.environ.get('ENABLE_SENTRY_TRACE', None) == 'true' and os.environ.get('SENTRY_DSN', None):
            try:
                import sentry_sdk
            except:
                raise ImportError("sentry-sdk is not installed.")
            self.sentry_trace = True
        else:
            self.sentry_trace = False

        if self.sentry_trace:
            tracer = None
        else:
            if not (tracer_provider := kwargs.get("tracer_provider")):
                tracer_provider = trace.get_tracer_provider()

            tracer = trace.get_tracer(
                instrumenting_module_name=__name__,
                tracer_provider=tracer_provider,
            )

        # 保存原始函数的引用

        try:
            from .tracer_wrapper import  (
                session_post_func, 
                client_run_trace_func,
                client_tool_trace_func, 
                assistent_tool_trace_func, 
                assistant_run_trace_func,
                assistent_stream_run_trace_func,
                assistant_stream_run_with_handler_trace_func,
                components_run_trace_func,
                components_run_stream_trace_func,
                list_trace_func,
                )
            self._original_session_post = session_post_func
            self._original_client_run = client_run_trace_func
            self._original_client_tool =  client_tool_trace_func
            self._original_assistant_tool = assistent_tool_trace_func
            self._original_assistant_run = assistant_run_trace_func
            self._original_assistant_stream_run = assistent_stream_run_trace_func
            self._original_assistant_stream_run_with_handler = assistant_stream_run_with_handler_trace_func
            self._orignal_components_run = components_run_trace_func
            self._original_components_stream_run = components_run_stream_trace_func
            self._original_list = list_trace_func
        except:
            raise ImportError(
                "Please check if the run_trace, tool_eval_streaming_trace, and assistant_trace methods are missing from the file.")

        # 保证trace对appbuilder与appbuilder-sdk-ext的兼容性
        try:
            appbuilder = import_module(_MODULE_1)
        except:
            appbuilder = None

        
        def _appbuilder_session_post(wrapped, instance, args, kwargs):
            return _post_trace(tracer, self._original_session_post, *args, **kwargs)
        
        def _appbuilder_client_run_trace(wrapped, instance, args, kwargs):
            return _client_run_trace(tracer, self._original_client_run, *args, **kwargs)
        
        def _appbuilder_client_tool_trace(wrapped, instance, args, kwargs):
            return _client_tool_trace(tracer, self._original_client_tool, *args, **kwargs)
        
        def _appbuilder_assistant_tool_trace(wrapped, instance, args, kwargs):
            return _assistant_tool_trace(tracer, self._original_assistant_tool, *args, **kwargs)
        
        def _appbuilder_assistant_run_trace(wrapped, instance, args, kwargs):
            return _assistant_run_trace(tracer, self._original_assistant_run, *args, **kwargs)
        
        def _appbuilder_assistant_stream_run_trace(wrapped, instance, args, kwargs):
            return _assistant_stream_trace(tracer, self._original_assistant_stream_run, *args, **kwargs)
        
        def _appbuilder_assistant_stream_run_with_handler_trace(wrapped, instance, args, kwargs):
            return _assistant_stream_run_with_handler_trace(tracer, self._original_assistant_stream_run_with_handler, *args, **kwargs)
        
        def _appbuilder_components_run_trace(wrapped, instance, args, kwargs):
            return _components_run_trace_with_opentelemetry(tracer, self._orignal_components_run, *args, **kwargs)

        def _appbuilder_components_run_trace_with_sentry(wrapped, instance, args, kwargs):
            return _components_run_trace_with_sentry(self._orignal_components_run, *args, **kwargs)
        
        def _appbuilder_components_run_stream_trace(wrapped, instance, args, kwargs):
            return _components_stream_run_trace_with_opentelemetry(tracer, self._original_components_stream_run, *args, **kwargs)
        
        def _appbuilder_components_run_stream_trace_with_sentry(wrapped, instance, args, kwargs):
            return _components_stream_run_trace_with_sentry(self._original_components_stream_run, *args, **kwargs)
        
        def _appbuilder_list_trace(wrapped, instance, args, kwargs):
            return _list_trace(tracer, self._original_list, *args, **kwargs)

        # 引用相关函数并替换
        if appbuilder:
            if not self.sentry_trace:
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

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.assistent_tool_trace_func',
                    wrapper= _appbuilder_assistant_tool_trace
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.assistant_run_trace_func',
                    wrapper= _appbuilder_assistant_run_trace
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.assistent_stream_run_trace_func',
                    wrapper= _appbuilder_assistant_stream_run_trace
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.assistant_stream_run_with_handler_trace_func',
                    wrapper= _appbuilder_assistant_stream_run_with_handler_trace
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.list_trace_func',
                    wrapper= _appbuilder_list_trace
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.components_run_trace_func',
                    wrapper= _appbuilder_components_run_trace
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.components_run_stream_trace_func',
                    wrapper= _appbuilder_components_run_stream_trace
                )
            else:
                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.components_run_trace_func',
                    wrapper= _appbuilder_components_run_trace_with_sentry
                )

                wrap_function_wrapper(
                    module= _MODULE_1, 
                    name = 'utils.trace.tracer_wrapper.components_run_stream_trace_func',
                    wrapper= _appbuilder_components_run_stream_trace_with_sentry
                )

        if not appbuilder:
            raise Exception("appbuilder not found")

    def _uninstrument(self):
        """
        恢复原始函数，移除之前添加的追踪代码。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        Raises:
            无异常抛出，但如果在尝试恢复原始函数时遇到任何问题，将打印一条错误消息"appbuilder not found"。
        
        """
        # 恢复原始函数
        try:
            from appbuilder.utils.trace.tracer_wrapper import (
                session_post_func, 
                client_run_trace_func, 
                client_tool_trace_func, 
                assistent_tool_trace_func, 
                assistant_run_trace_func,
                assistant_stream_run_with_handler_trace_func,
                components_run_trace_func,
                components_run_stream_trace_func,
                list_trace_func,
                )
            
            session_post_func = self._original_session_post
            client_run_trace_func = self._original_client_run
            client_tool_trace_func = self._original_client_tool
            assistent_tool_trace_func = self._original_assistant_tool
            assistant_run_trace_func = self._original_assistant_run
            assistant_stream_run_with_handler_trace_func = self._original_assistant_stream_run_with_handler
            components_run_trace_func = self._orignal_components_run
            components_run_stream_trace_func = self._original_components_stream_run
            list_trace_func = self._original_list
        except:
            print("appbuilder not found")
            

def create_tracer_provider(enable_phoenix: bool = True, enable_console: bool = False, host: str = "127.0.0.1", port: int = 8080, method: str = "/v1/traces"):
    """
    创建一个用于跟踪的TracerProvider对象，并可选择性地添加span处理器，以便将跟踪数据发送到指定的端点或控制台。
    
    Args:
        enable_phoenix (bool, optional): 是否启用Phoenix，以在本地可视化界面展示trace数据。默认为True。
        enable_console (bool, optional): 是否启用控制台输出，以在控制台展示trace数据。默认为False。
        host (str, optional): Phoenix可视化界面的主机地址。默认为"127.0.0.1"。
        port (int, optional): Phoenix可视化界面的端口号。默认为8080。
        method (str, optional): Phoenix可视化界面的请求路径。默认为"/v1/traces"。
    
    Returns:
        TracerProvider: 创建的TracerProvider对象，可用于创建跟踪的Span对象。
    
    """
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
    _instance = None
    _trace_start = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, enable_phoenix: bool = True, enable_console: bool = False, host: str = "http://localhost", port: int = 8080, method="/v1/traces") -> None:
        """
        初始化函数，用于设置追踪系统相关参数。
        
        Args:
            enable_phoenix (bool, optional): 是否启用Phoenix服务。默认为True。
            enable_console (bool, optional): 是否启用控制台输出。默认为False。
            host (str, optional): 可视化追踪系统服务的地址。默认为"http://localhost"。
            port (int, optional): 可视化追踪系统服务的端口号。默认为8080。
            method (str, optional): 可视化追踪系统服务的方法路径。默认为"/v1/traces"。
        
        Returns:
            None: 无返回值。
        
        """
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
        if self._trace_start:
            return
        logger.info("AppBuilder Starting trace...")
        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "true"
        self._instrumentor._instrument(tracer_provider=self._tracer_provider)

    def end_trace(self):
        logger.info("AppBuilder Ending trace...")
        del os.environ["APPBUILDER_SDK_TRACE_ENABLE"]
        self._instrumentor._uninstrument()

    def __enter__(self):
        self.start_trace()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_trace()
