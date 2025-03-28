# MCP Component Server

The MCP Component Server is a FastMCP server based implementation that converts AppBuilder Components into FastMCP tools, enabling seamless integration of Baidu cloud AI services into MCP-compatible environments.

## Overview

The `MCPComponentServer` class provides a bridge between AppBuilder Components and FastMCP tools, allowing you to:
- Convert AppBuilder Components into MCP-compatible tools
- Handle various content types (text, images, audio, references)
- Manage visibility scopes for different audiences
- Support streaming responses through generators

## Features

- Automatic conversion of AppBuilder Components to MCP tools
- Support for multiple content types:
  - Text content
  - Image content
  - Audio content
  - Reference content
- Configurable host and port settings
- Built-in error handling and logging
- Support for custom tool registration
- Automatic MIME type detection for media content

## Usage

### Basic Setup

```python
from appbuilder import GeneralOCR, TextGeneration
from mcp.server import MCPComponentServer

# Create server instance
server = MCPComponentServer("AI Service", host="localhost", port=8000)

# Add AppBuilder components
ocr = GeneralOCR()
server.add_component(ocr)

text_gen = TextGeneration()
server.add_component(text_gen)

# Run the server
server.run()
```

### Adding Custom Tools

```python
@server.tool()
def custom_function(param1: str, param2: int) -> str:
    """Custom tool description"""
    return f"Processed: {param1} {param2}"
```

### Adding Resources

```python
@server.resource()
def get_resource():
    """Resource description"""
    return {"data": "resource content"}
```

## Content Type Handling

The server automatically handles various content types:

1. **Text Content**: Converts text outputs to MCP TextContent
2. **Image Content**: Handles both base64 and URL-based images
3. **Audio Content**: Processes audio files with automatic MIME type detection
4. **Reference Content**: Manages document references and citations


## Configuration

The server can be configured with various parameters:

```python
server = MCPComponentServer(
    name="Service Name",
    host="localhost",  # Default: "localhost"
    port=8000,        # Default: 8000
    **kwargs          # Additional FastMCP arguments
)
```