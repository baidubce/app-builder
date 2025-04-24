# App MCP Server

App MCP Server provides a set of tools for using Agent from AppBuilder through the MCP protocol. It allows you to list apps, create conversations, run with AppBuilder Agent.

## Features

* **List Apps**: Get your AppBuilder application list.
* **Create Conversation**: Create a new conversation_id, which is valid for 7 days. After that, it may not work and needs to be regenerated.
* **Run**: Send messages to the agent application during a conversation.

## Quick Start

1. Get your AppBuilder API Key from the console
2. Format your authorization token as: `Bearer+<AppBuilder API Key>` (keep the "+" in between)
3. Config with

```json
{
  "mcpServers": {
    "appbuilder-app": {
      "url": "http://appbuilder.baidu.com/v2/app/mcp/sse?api_key=Bearer+bce-v3/ALTAK..."
    }
  }
}
```

## Available Tools

### get_all_apps

Retrieve a list of all available AppBuilder applications.

**Parameters:**
No parameter required

**Returns:**
- List of dictionaries, each containing an app's id, name, and description.

### create_conversation

Create a new conversation session for a specific AppBuilder application.

**Parameters:**
- `app_id` (str): ID of the Application.

**Returns:**
- `converstaion_id`(str) : ID of the conversation.

### run

Execute a conversation query with a specific AppBuilder application.

**Parameters:**
- `app_id` (str): The unique identifier of the target application
- `conversation_id `(str): The conversation session identifier
- `query `(str): The input text/query to send to the application

**Returns:**
- The response content from the conversation

## Usage Examples

### Get your AppBuilder application list

```python
import asyncio
import os
import json
from appbuilder.mcp_server.client import MCPClient

os.environ["APPBUILDER_TOKEN"] = "YOUR_APPBUILDER_TOKEN"

async def main():
    client = MCPClient()
    await client.connect_to_server(service_url=service_url)
    print(client.tools)
    result = await client.call_tool(
        "get_all_apps", {}
    )
    print(result)

if __name__ == "__main__":
    service_url = "http://appbuilder.baidu.com/v2/app/mcp/sse?api_key=Bearer+" + os.environ.get("APPBUILDER_TOKEN")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

### Chat with AppBuilder Application

```python
import asyncio
import json
import os
from appbuilder.mcp_server.client import MCPClient

os.environ["APPBUILDER_TOKEN"] = "YOUR_APPBUILDER_TOKEN"
os.environ["APP_ID"] = "YOUR_APP_ID"

async def main():    
    client = MCPClient()
    await client.connect_to_server(service_url=service_url)
    app_id = os.environ.get("APP_ID")
    result = await client.call_tool(
        "create_conversation", {"app_id": app_id}
    )
    conversation_id = result.content[0].text
    print(conversation_id)
    result = await client.call_tool(
        "run",
        {
            "app_id": app_id,
            "conversation_id": conversation_id,
            "query": "hello",
        },
    )
    print(result.content[0].text)

if __name__ == "__main__":
    service_url = "http://appbuilder.baidu.com/v2/app/mcp/sse?api_key=Bearer+" + os.environ.get("APPBUILDER_TOKEN")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

