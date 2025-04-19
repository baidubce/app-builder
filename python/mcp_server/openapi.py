from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Callable, Awaitable
import asyncio
import yaml
import json
import aiohttp
from .http_client import HTTPClient

@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: Dict[str, Any]
    operation_id: str
    method: str
    path: str
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]] = None

    def create_handler(self, converter: 'OpenAPIMCPConverter') -> Callable:
        """
        Create a handler function for this tool that can be registered with MCP.

        Returns:
            Callable: An async function that handles tool execution
        """
        async def handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
            # Prepare request parameters
            url = self.path
            query_params = {}
            headers = {}
            body = None

            # Handle path parameters
            for param in self.parameters:
                if 'name' not in param:
                    continue

                param_name = param['name']
                if param_name in arguments:
                    value = arguments[param_name]

                    # Convert to string if needed
                    if isinstance(value, (int, float, bool)):
                        value = str(value)

                    if param.get('in') == 'path':
                        url = url.replace(f"{{{param_name}}}", value)
                    elif param.get('in') == 'query':
                        query_params[param_name] = value
                    elif param.get('in') == 'header':
                        headers[param_name] = value

            # Handle request body
            if self.request_body:
                content_type = next(iter(self.request_body['content'].keys()))
                body_schema = self.request_body['content'][content_type]['schema']
                body = {}

                for prop_name in body_schema.get('properties', {}):
                    if prop_name in arguments:
                        body[prop_name] = arguments[prop_name]

            # Make the API call using the converter's HTTP client
            response = await converter.http_client.request(
                method=self.method,
                url=url,
                params=query_params,
                headers=headers,
                json=body if body else None
            )

            return response

        # Set metadata on the handler
        handler.__name__ = self.name
        handler.__doc__ = self.description

        return handler

class OpenAPIMCPConverter:
    def __init__(self,
                 base_url: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None,
                 timeout: float = 30.0,
                 max_retries: int = 3):
        """
        Initialize the converter

        Args:
            base_url: Base URL for API calls
            headers: Default headers for API calls
            timeout: Timeout for API calls in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.tools: Dict[str, MCPTool] = {}
        self.http_client = HTTPClient(
            base_url=base_url,
            headers=headers,
            default_timeout=timeout,
            max_retries=max_retries
        )

    def create_tools(self, prefix: str = "") -> Dict[str, Callable]:
        """
        Create callable handlers for all tools with optional prefix

        Args:
            prefix: Optional prefix to add to tool names

        Returns:
            Dict[str, Callable]: Dictionary of tool name to handler function
        """
        handlers = {}
        for tool_name, tool in self.tools.items():
            prefixed_name = f"{prefix}{tool_name}" if prefix else tool_name
            handlers[prefixed_name] = tool.create_handler(self)
        return handlers

    async def close(self) -> None:
        """Close the HTTP client session"""
        await self.http_client.close()

    async def load_spec(self, spec_source: str) -> None:
        """
        Load OpenAPI spec from URL or file

        Args:
            spec_source: URL or file path to OpenAPI spec
        """
        if spec_source.startswith(('http://', 'https://')):
            # Use HTTP client to fetch the spec
            response = await self.http_client.get(spec_source)

            if not response.get('success', False):
                error = response.get('error', {})
                raise Exception(f"Failed to load spec: {error.get('detail', 'Unknown error')}")

            # Parse the response data
            if isinstance(response['data'], dict):
                spec = response['data']
            else:
                # If data is not a dict, try to parse it as JSON
                spec = json.loads(response['data'])
        else:
            with open(spec_source, 'r', encoding='utf-8') as f:
                if spec_source.endswith(('.yaml', '.yml')):
                    spec = yaml.safe_load(f)
                else:
                    spec = json.load(f)

        # Set base URL if not provided
        if not self.base_url and 'servers' in spec:
            self.base_url = spec['servers'][0]['url']
            # Update HTTP client with new base_url
            self.http_client.base_url = self.base_url

        await self._process_spec(spec)

    async def _process_spec(self, spec: Dict[str, Any]) -> None:
        """Process OpenAPI spec and create MCP tools"""
        for path, path_item in spec['paths'].items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                    continue

                tool = self._create_tool(path, method, operation)
                self.tools[tool.name] = tool

    def _create_tool(self, path: str, method: str, operation: Dict[str, Any]) -> MCPTool:
        """Create MCPTool from OpenAPI operation"""
        # Use operationId if available, otherwise create from method and path
        operation_id = operation.get('operationId') or f"{method}_{path}"

        # Collect parameters
        parameters = operation.get('parameters', [])
        required_params = []

        # Build input schema
        properties = {}
        for param in parameters:
            # Skip parameters without a name
            if 'name' not in param:
                print(f"Warning: Parameter without name in {path} {method}")
                continue

            param_name = param['name']
            if param.get('required', False):
                required_params.append(param_name)

            param_schema = param.get('schema', {}).copy()  # Create a copy to modify

            # Handle parameter enums
            if 'enum' in param_schema:
                param_schema['enum'] = [str(v) for v in param_schema['enum']]

            # Handle parameter types
            if param_schema.get('type') == 'integer':
                param_schema['type'] = ['integer', 'string']  # Allow string input for integers

            properties[param_name] = {
                'type': param_schema.get('type', 'string'),
                'description': param.get('description', ''),
                'required': param.get('required', False)
            }

            # Add enum values if present
            if 'enum' in param_schema:
                properties[param_name]['enum'] = param_schema['enum']

        # Add request body if present
        if 'requestBody' in operation:
            content = operation['requestBody']['content']
            if 'application/json' in content:
                body_schema = content['application/json']['schema']
                if 'properties' in body_schema:
                    for prop_name, prop_schema in body_schema['properties'].items():
                        properties[prop_name] = {
                            'type': prop_schema.get('type', 'string'),
                            'description': prop_schema.get('description', ''),
                            'required': prop_name in body_schema.get('required', [])
                        }
                        if 'enum' in prop_schema:
                            properties[prop_name]['enum'] = prop_schema['enum']

        input_schema = {
            'type': 'object',
            'properties': properties,
            'required': required_params
        }

        return MCPTool(
            name=operation_id,
            description=operation.get('summary', operation.get('description', '')),
            input_schema=input_schema,
            operation_id=operation_id,
            method=method,
            path=path,
            parameters=parameters,
            request_body=operation.get('requestBody')
        )

    def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of tools in MCP format"""
        return [
            {
                'name': tool.name,
                'description': tool.description,
                'input_schema': tool.input_schema
            }
            for tool in self.tools.values()
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None, max_retries: int = None, timeout: int = None) -> Dict[str, Any]:
        """Execute tool by making API call"""
        if arguments is None:
            arguments = {}

        if tool_name not in self.tools:
            return {
                'error': {
                    'type': 'tool_not_found',
                    'detail': f"Tool '{tool_name}' not found"
                }
            }

        tool = self.tools[tool_name]

        # Prepare request parameters
        url = tool.path
        query_params = {}
        headers = {}

        # Handle path parameters
        for param in tool.parameters:
            # Skip parameters without a name
            if 'name' not in param:
                continue

            param_name = param['name']
            if param_name in arguments:
                value = arguments[param_name]

                # Convert to string if needed
                if isinstance(value, (int, float, bool)):
                    value = str(value)

                if param.get('in') == 'path':
                    url = url.replace(f"{{{param_name}}}", value)
                elif param.get('in') == 'query':
                    query_params[param_name] = value
                elif param.get('in') == 'header':
                    headers[param_name] = value

        # Handle request body
        if tool.request_body:
            body_params = {
                k: v for k, v in arguments.items()
                if k not in query_params and k not in headers
            }
            if body_params:
                json_data = body_params
            else:
                json_data = None
        else:
            json_data = None

        # Make the request using our HTTP client
        response = await self.http_client.request(
            method=tool.method,
            url=url,
            params=query_params,
            headers=headers,
            json_data=json_data,
            timeout=timeout,
            max_retries=max_retries
        )

        # Handle the response
        if response.get('success', False):
            result = response['data']
            return {
                'content': [
                    {
                        'type': 'json' if isinstance(result, (dict, list)) else 'text',
                        'json' if isinstance(result, (dict, list)) else 'text': result
                    }
                ]
            }
        else:
            # Return the error information
            return {
                'error': response.get('error', {
                    'type': 'unknown_error',
                    'detail': 'Unknown error occurred'
                })
            }



