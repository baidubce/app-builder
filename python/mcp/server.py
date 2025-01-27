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


from typing import Type, Optional, Any, Dict, List, Literal
from appbuilder.core.component import Component, ComponentOutput
from appbuilder.core.message import Message
import logging

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise ImportError(
        "Could not import FastMCP. Please install MCP package with: "
        "pip install mcp"
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
        if not base_url.startswith('/'):
            base_url = '/' + base_url
        if not base_url.endswith('/'):
            base_url = base_url + '/'

        # Register each manifest as a separate tool under the component's URL
        for manifest in component.manifests:
            tool_name = manifest["name"]
            
            def create_tool_fn(comp: Component, tool_manifest: dict):
                def tool_fn(**kwargs) -> Any:
                    try:
                        # Try tool_eval first
                        if hasattr(comp, "tool_eval"):
                            results = []
                            for output in comp.tool_eval(**kwargs):
                                if isinstance(output, ComponentOutput):
                                    for content in output.content:
                                        if content.type == "text":
                                            results.append(content.text.info)
                                        elif content.type == "json":
                                            results.append(content.text.data)
                            return "\n".join(results) if results else None
                        
                        # Fall back to run method
                        msg = Message(content=kwargs)
                        result = comp.run(msg)
                        return result.content
                        
                    except Exception as e:
                        logger.error(f"Error in {tool_name}: {str(e)}")
                        raise

                return tool_fn

            # Create tool function with metadata
            tool_fn = create_tool_fn(component, manifest)
            tool_fn.__name__ = tool_name
            tool_fn.__doc__ = manifest["description"]

            # Register parameter types from manifest
            param_types = {}
            required_params = set()
            
            # Get required parameters
            if "required" in manifest["parameters"]:
                required_params.update(manifest["parameters"]["required"])
                
            # Add parameter info
            for param_name, param_info in manifest["parameters"]["properties"].items():
                param_type = self._convert_json_schema_type(param_info["type"])
                param_types[param_name] = param_type
                if param_name in required_params:
                    param_types[f"_{param_name}_is_required"] = True

            tool_fn.__annotations__ = param_types

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
            "object": Dict
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
    from appbuilder import SimilarQuestion, StyleRewrite, OralQueryGeneration
    from appbuilder.mcp.server import MCPComponentServer

    os.environ["APPBUILDER_TOKEN"] = 'bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd'

    # Create server with host and port arguments
    server = MCPComponentServer("AI Services", host="localhost", port=8888)

    model = "ERNIE-4.0-8K"
    server.add_component(SimilarQuestion(model=model)) # served at /similar_question/
    server.add_component(StyleRewrite(model=model)) # served at /style_rewrite/
    server.add_component(OralQueryGeneration(model=model)) # served at /query_generation/

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
    server.run()
