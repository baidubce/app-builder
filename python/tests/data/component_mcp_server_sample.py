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

import json
from appbuilder.core.component import Component
from typing import Type, Optional, Any, Dict, List, Literal, Sequence
from itertools import chain
import logging
import inspect
import pydantic_core
from functools import wraps

logging.basicConfig(level=logging.INFO)

try:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp.utilities.types import Image
    from mcp.types import (
        EmbeddedResource,
        ImageContent,
        TextContent,
    )
except ImportError:
    raise ImportError(
        "Could not import FastMCP. Please install MCP package with: " "pip install mcp"
    )


logger = logging.getLogger(__name__)


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

    def __init__(
        self, name: str, host: str = "localhost", port: int = 8000, **kwargs: Any
    ):
        """
        Initialize the ComponentMCPServer.

        Args:
            name (str): Name of the server
            host (str): Host address to bind to (default: "localhost")
            port (int): Port number to listen on (default: 8000)
            **kwargs: Additional arguments passed to FastMCP
        """
        self.mcp = FastMCP(name, host=host, port=port, **kwargs)
        self.components: Dict[str, Component] = {}

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

    def _convert_to_content(
        self,
        result: Any,
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Convert a result to a sequence of content objects."""
        if result is None:
            return []

        if isinstance(result, (TextContent, ImageContent, EmbeddedResource)):
            return [result]

        if isinstance(result, Image):
            return [result.to_image_content()]

        if isinstance(result, (list, tuple)):
            return list(
                chain.from_iterable(self._convert_to_content(item) for item in result)
            )

        if not isinstance(result, str):
            try:
                result = json.dumps(result.model_dump())
            except Exception:
                result = str(result)

        return [TextContent(type="text", text=result)]

    def add_component(self, component: Component, url: Optional[str] = None) -> None:
        """
        Add an Appbuilder Component and register its tools under the component's URL namespace.

        Args:
            component (Component): The component instance to add
            url (str, optional): Custom URL to override component's default URL.
                               If not provided, uses /{component.name}/
        """
        # Store component instance
        component_type = type(component).__name__
        self.components[component_type] = component

        # Use component's name for URL if not overridden
        base_url = url if url is not None else f"/{component.name}/"

        # Ensure URL starts and ends with /
        if not base_url.startswith("/"):
            base_url = "/" + base_url
        if not base_url.endswith("/"):
            base_url = base_url + "/"

        # Register each manifest as a separate tool under the component's URL
        for manifest in component.manifests:
            tool_name = manifest["name"]
            signature = inspect.signature(component.tool_eval)

            def create_tool_fn(func):
                @wraps(func)
                def wrapper(*args, **kwargs) -> Any:
                    try:
                        # call tool_eval
                        results = []
                        bound_values = signature.bind(*args, **kwargs)
                        result = component.tool_eval(
                            *bound_values.args, **bound_values.kwargs
                        )
                        for output in result:
                            yield output
                            # if isinstance(output, ComponentOutput):
                            #     for content in output.content:
                            #         if content.type == "text":
                            #             results.append(content.text.info)
                            #         elif content.type == "json":
                            #             results.append(content.text.data)
                        # return "\n".join(results) if results else None

                    except Exception as e:
                        logger.error(f"Error in {tool_name}: {str(e)}")
                        raise

                wrapper.__signature__ = signature
                return wrapper

            # Create tool function with metadata
            tool_fn = create_tool_fn(component.tool_eval)
            tool_fn.__name__ = tool_name
            tool_fn.__doc__ = manifest["description"]

            # Register with FastMCP using name and description from manifest
            self.mcp.tool(name=tool_name, description=manifest["description"])(tool_fn)

    def _convert_json_schema_type(self, json_type: str) -> Type:
        """Convert JSON schema type to Python type"""
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": List,
            "object": Dict,
        }
        return type_mapping.get(json_type, Any)

    def run(self, transport: Literal["stdio", "sse"] = "stdio") -> None:
        """Run the FastMCP server. Note this is a synchronous function.

        Args:
            transport: Transport protocol to use ("stdio" or "sse")
        """
        self.mcp.run()


if __name__ == "__main__":
    import os
    from appbuilder.core.components.v2 import (
        Translation,
        StyleWriting,
        OralQueryGeneration,
        
    )


    os.environ["APPBUILDER_TOKEN"] = (
        "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"
    )

    # Create server with host and port arguments
    server = MCPComponentServer("AI Services", host="localhost", port=8888)

    model = "ERNIE-4.0-8K"
    server.add_component(Translation())  # served at /similar_question/
    server.add_component(StyleWriting(model=model))  # served at /style_rewrite/
    server.add_component(
        OralQueryGeneration(model=model)
    )  # served at /query_generation/

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

    # Run server
    server.run(transport="sse")
