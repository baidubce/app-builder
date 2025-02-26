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
from appbuilder.core.component import Component, Image, Audio, References, Content
from appbuilder.core._exception import *
from typing import Any, Literal
from collections.abc import Generator
import logging
import inspect
import requests
import base64
import io
from functools import wraps
logging.basicConfig(level=logging.INFO)

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp.server import _convert_to_content
    from mcp.types import (
        ImageContent,
        TextContent,
        EmbeddedResource,
        TextResourceContents,
        BlobResourceContents,
        Annotations
    )
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

    def _convert_visible_scope_to_audience(
        self,
        visible_scope: str
    ) -> list[str]:
        if visible_scope == "llm":
            return ["assistant"]
        elif visible_scope == "user":
            return ["user"]
        else:
            return ["user", "assistant"]

    def _convert_image_to_image_content(
            self, 
            text: Image,
            audience: list[str]
        ) -> ImageContent:
        """convert base64 data, such as image/audio  to ImageContent"""

        def _get_mime_type(image_data: bytes) -> str:
            """get mime_type of image"""
            import imghdr
            image_type = imghdr.what(image_data)
            mime_type = f"image/{image_type}"
            return mime_type
        
        try:
            if text.byte:
                logging.info("create ImageContent from Image.byte")
                base64_data = base64.b64encode(text.byte).decode("utf-8")
                mime_type = _get_mime_type(text.byte)
            else:
                logging.info("create ImageContent from Image.url")
                response = requests.get(text.url)
                response.raise_for_status()
                image = response.content
                base64_data = base64.b64encode(image).decode('utf-8')

                image_byte = io.BytesIO(image)
                mime_type = _get_mime_type(image_byte)
                
            # create ImageContent
            return ImageContent(
                type="image",
                data=base64_data,
                mimeType=mime_type,
                annotations=Annotations(
                    audience=audience
                )
            )
        except Exception as e:
            logging.error("failed convet image to ImageContent")
            raise e

    def _convert_audio_to_embedded_resource(
        self,
        text: Audio,
        audience: str = Literal["user", "assistant"]
    ) -> EmbeddedResource:
        """convert audio to EmebeddedResource"""
        def detect_audio_type(data: bytes) -> str:
            import filetype
            kind = filetype.guess(data)
            return kind.extension if kind else "未知格式"

        try:
            if text.byte:
                logging.info("convert audio to EmbeddedResource from Audio.byte")
                base64_data = base64.b64encode(text.byte).decode("utf-8")
                audio_type = detect_audio_type(text.byte)

            else:
                logging.info("convert audio to EmbeddedResource from Audio.url")
                # get data
                response = requests.get(text.url)
                response.raise_for_status()
                # convert to base64
                base64_data = base64.b64encode(response.content).decode('utf-8')
                # detect audio type
                audio_byte = io.BytesIO(response.content)
                audio_type = detect_audio_type(audio_byte)
                
            # create EmbeddedResource
            return EmbeddedResource(
                type="resource",
                resource=BlobResourceContents(
                    blob=base64_data,
                    uri=text.url,
                    mimeType="audio/" + audio_type,
                ),
                annotations=Annotations(
                    audience=audience
                )
            )
        except Exception as e:
            logging.error("failed to convert audio to EmbeddedResource")
            raise e
        
    def _convert_reference_to_embedded_resource(
        self,
        text: References,
        audience: str = Literal["user", "assistant"]
    ) -> EmbeddedResource:
        """convert reference to EmbeddedResource"""
        from urllib.parse import unquote
        return EmbeddedResource(
            type="resource",
            resource=TextResourceContents(
                uri=unquote(text.doc_id),
                text=text.content,
                mimeType="references/" + text.source
            ),
            annotations=Annotations(
                audience=audience
            )
        )

    def _convert_component_output_to_text_content(
        self,
        text: Content,
        audience: str = Literal["user", "assistant"]
    ) -> TextContent:
        """convert ComponentOutput to json_str"""
        return TextContent(
            type="text",
            text=text.model_dump_json(),
            annotations=Annotations(
                audience=audience
            )
        )

    def _convert_generator(
        self,
        result: Generator
    ) -> list[TextContent|ImageContent|EmbeddedResource]:
        """convert geneartor to list of TextContent, ImageContent and EmbeddedResource"""
        output = []
        for iter in result:
            type = iter.content[0].type
            text = iter.content[0].text
            visible_scope = iter.content[0].visible_scope
            audience = self._convert_visible_scope_to_audience(visible_scope)
            if type in ["text", "oral_text"]:
                text_output = TextContent(
                    type="text", 
                    text=iter.content[0].text.info, 
                    annotations=Annotations(
                        audience=audience
                    )
                )
                output.append(text_output)
            elif type == "audio":
                audio_output = self._convert_audio_to_embedded_resource(text, audience)
                output.append(audio_output) 
            else:
                match type:
                    case "image":
                        image_output = self._convert_image_to_image_content(text, audience)
                        output.append(image_output)
                    case "references":
                        reference_output = self._convert_reference_to_embedded_resource(
                            text,
                            audience
                        )
                        output.append(reference_output)
                iter_output = self._convert_component_output_to_text_content(iter.content[0], audience)
                output.append(iter_output)
        output = _convert_to_content(output)
        logging.info(f"output: {output}")
        return output


    def add_component(self, component: Component) -> None:
        """
        Add an Appbuilder Component and register its tools under the component's URL namespace.

        Args:
            component (Component): The component instance to add
        """

        # Register each manifest as a separate tool
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
                        if result is NotImplementedError:
                            logging.error(f"tool_eval not implemented in {tool_name}")
                            raise NotImplementedError(f"tool_eval not implemented in {tool_name}")
                        
                        list_result = self._convert_generator(result)
                        return list_result
                    
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

    def add_appbuilder_official_tool(
            self,
            component_cls: Component,
            init_args: dict[str, Any] = {},
        ):
        """add AppBuilder official tool as MCP server"""
        component_name = component_cls.__name__
        logging.info(f"init {component_name} with args: {init_args}")

        try:    
            component = component_cls(**init_args)
            self.add_component(component)
            logging.info(f"component: {component_name} has been added")
            
        except Exception as e:
            logging.exception(f"Failed to add component {component_name}: {str(e)}")
            raise e

    def run(self, transport: Literal["stdio", "sse"] = "stdio") -> None:
        """Run the FastMCP server. Note this is a synchronous function.

        Args:
            transport: Transport protocol to use ("stdio" or "sse")
        """
        self.mcp.run()


if __name__ == "__main__":
    from appbuilder.modelcontextprotocol.server import MCPComponentServer
    server = MCPComponentServer("AI Services")
    from appbuilder.core.components.v2 import Translation

    init_args = {
        "model": "ERNIE-4.0-8K",
        "secret_key": 'bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd'
    }
    server.add_appbuilder_official_tool(Translation, init_args)
    

    # Add custom tool
    @server.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    # Add dynamic resource
    @server.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting"""
        return f"Hello, {name}!"

    server.run()


    
