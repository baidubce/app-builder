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

import appbuilder
from appbuilder.core.component import Component
from appbuilder.core._exception import *
from typing import Any, Literal
import logging
import inspect
from functools import wraps
logging.basicConfig(level=logging.INFO)

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.types import ImageContent
except ImportError:
    raise ImportError(
        "Could not import FastMCP. Please install MCP package with: "
        "pip install mcp"
    )

class MCPComponentServer:
    """
    A server that converts Appbuilder Components to FastMCP tools.
    
    Examples:
    
    .. code-block:: python
    
        # Create server
        server = MCPComponentServer("AI Service")
        
        # Add components with default URLs based on their names
        ocr = GeneralOCR()
        server.add_component(ocr)  # Will use default URL based on component name
        
        # Add component with custom URL
        text_gen = TextGeneration() 
        server.add_component(text_gen)  # Will use default URL based on component name
        
        # Add custom tool
        @server.tool()
        def add(a: int, b: int) -> int:
            '''Add two numbers'''
            return a + b
            
        # Run server
        server.run()
    """

    def __init__(self, name: str, host: str = "localhost", port: int = 8000, **kwargs: Any):
        """
        Initialize the ComponentMCPServer.

        Args:
            name (str): Name of the server
            host (str): Host address to bind to (default: "localhost")
            port (int): Port number to listen on (default: 8000)
            **kwargs: Additional arguments passed to FastMCP
        """
        self.mcp = FastMCP(name, host=host, port=port, **kwargs)
        self.components = {}

    def tool(self, *args, **kwargs):
        """
        Decorator to register a custom tool function.
        Passes through to FastMCP's tool decorator.

        Args:
            *args: Positional arguments for FastMCP tool decorator
            **kwargs: Keyword arguments for FastMCP tool decorator
        """
        return self.mcp.tool(*args, **kwargs)

    def resource(self, *args, **kwargs):
        """
        Decorator to register a resource.
        Passes through to FastMCP's resource decorator.

        Args:
            *args: Positional arguments for FastMCP resource decorator
            **kwargs: Keyword arguments for FastMCP resource decorator
        """
        return self.mcp.resource(*args, **kwargs)

    def _convert_image_output(self, url: str) -> ImageContent:
        import requests
        import base64
        import imghdr
        import io
        
        # 获取图片数据
        response = requests.get(url)
        image_bytes = response.content
        
        # 获取图片类型并构造 mimeType
        image_data = io.BytesIO(image_bytes)
        image_type = imghdr.what(image_data)
        mime_type = f"image/{image_type}"
        
        # 转换为base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # 创建 ImageContent
        return ImageContent(
            type="image",
            data=image_base64,
            mimeType=mime_type
        )

    def add_component(self, component: Component) -> None:
        """
        Add an Appbuilder Component and register its tools under the component's URL namespace.

        Args:
            component (Component): The component instance to add
            url (str, optional): Custom URL to override component's default URL. 
                               If not provided, uses /{component.name}/
        """

        # Register each manifest as a separate tool under the component's URL
        for manifest in component.manifests:
            tool_name = manifest["name"]
            tool_decription = manifest["description"]
            def create_tool_fn(func):
                signature = inspect.signature(func)
                @wraps(func)
                def wrapper(*args, **kwargs) -> Any:
                    try:
                        # call tool_eval
                        bound_values = signature.bind(*args, **kwargs)
                        result = func(*bound_values.args, **bound_values.kwargs)
                        for output in result:
                            if output.content[0].type == "image":
                                return self._convert_image_output(output.content[0].text.url)
                            else:
                                return output
                    
                    except Exception as e:
                        logging.error(f"Error in {tool_name}: {str(e)}")
                        raise
                wrapper.__signature__ = signature
                return wrapper

            # Create tool function with metadata
            tool_fn = create_tool_fn(component.tool_eval)
            tool_fn.__name__ = tool_name
            tool_fn.__doc__ = tool_decription

            # Register with FastMCP using name and description from manifest
            self.mcp.tool(name=tool_name, description=tool_decription)(tool_fn)

    def init_component(
            self,
            import_path: str = "appbuilder.core.components.v2.",
            component_init_args: dict[str, Any] = {},
            component_name: str = "",
        ) -> Component:
        """init component

        Args:
            relative_path (str, optional): path to import component. Defaults to "appbuilder.components.v2.".
            init_args (dict[str, Any], optional): init args. Defaults to {}.
            component_name (str, optional): component name to init. Defaults to "".

        Returns:
            Component: object of Component
        """
        if not component_name:
            logging.error("No component_name specified")
            raise InvalidRequestArgumentError("No component_name specified")
        
        try:
            import_res = eval(import_path + component_name)
        except Exception as e:
            logging.error(f"import component error: {e}")
            raise ImportError(f"import component error: {e}")

        try:
            component = import_res(**component_init_args)
        except Exception as e:
            logging.error(f"init component error: {e}")
            raise Exception(f"Failed to initialize component {component_name}: {str(e)}")
        return component

    def add_AppBuilder_tool(
            self,
            import_path: str = "appbuilder.core.components.v2.",
            component_list: list[str] = [],
            init_args: dict[str, Any] = {},
        ):
        """add AppBuilder tool as MCP server"""
        
        for component_name in component_list:
            try: 
                # 1. get component init args
                if component_name not in init_args:
                    component_init_args = {}
                else:
                    component_init_args = init_args[component_name]

                logging.info(f"init {component_name} with args: {component_init_args}")
                
                # 2. init component
                component = self.init_component(
                    import_path=import_path,
                    component_name=component_name,
                    component_init_args=component_init_args
                )
                
                # 3. add component
                self.add_component(component)
                logging.info(f"component: {component_name} has been added")
                
            except Exception as e:
                logging.exception(f"Failed to add component {component_name}: {str(e)}")
                continue

    def run(self, transport: Literal["stdio", "sse"] = "stdio") -> None:
        """Run the FastMCP server. Note this is a synchronous function.

        Args:
            transport: Transport protocol to use ("stdio" or "sse")
        """
        self.mcp.run()


def main():
    # from appbuilder.mcp.server import MCPComponentServer
    from appbuilder.core.components.v2 import __V2_COMPONENTS__
    server = MCPComponentServer("AI Services")
    model_config = {"model": "ERNIE-4.0-8K"}
    init_args = {
        "Translation": model_config,
        "AnimalRecognition": model_config,
        "Text2Image": model_config,
        "QRcodeOCR": model_config
    }
    
    server.add_AppBuilder_tool(
        import_path="appbuilder.core.components.v2.",  # 确保这个路径是正确的
        component_list=list(init_args.keys()),
        init_args=init_args
    )
    
    # # Add custom tool
    # @server.tool()
    # def add(a: int, b: int) -> int:
    #     """Add two numbers"""
    #     return a + b

    # # Add dynamic resource
    # @server.resource("greeting://{name}")
    # def get_greeting(name: str) -> str:
    #     """Get a personalized greeting"""
    #     return f"Hello, {name}!"

    server.run()


if __name__ == "__main__":
    import os
    os.environ["APPBUILDER_TOKEN"] = 'bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd'
    main()
    
