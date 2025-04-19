"""
Baidu AppBuilder MCP Server

This server provides MCP (Model Context Protocol) tools for interacting with Baidu AppBuilder applications.
It supports both stdio and SSE (Server-Sent Events) protocols.

SSE Access:
    URL: http://appbuilder.baidu.com/v2/ai_search/mcp/sse?api_key=<your api_key>

Authentication:
    - Requires an AppBuilder API key in the format "bce-v3/ALTAK-..."
    - Get your API key from: https://cloud.baidu.com/doc/AppBuilder/s/klv2eywua

Features:
    - List all available AppBuilder applications
    - Create new conversations with specific apps
    - Run with queries and get responses

Example Usage:
    1. Set your AppBuilder token:
       os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-..."
    
    2. Run the server:
       python app_server.py

    3. Use MCP client to interact with the server tools:
       - get_all_apps()
       - create_conversation(app_id)
       - run(app_id, conversation_id, query)
"""
import os
from typing import Optional, List, Dict
from mcp.server import FastMCP
import appbuilder
from appbuilder.core.component import Component

server = FastMCP(name="AppBuilder App MCP Server")


@server.tool()
def list_apps() -> List[Dict]:
    """
    Retrieve a list of all available AppBuilder applications.

    Returns:
        List[Dict]: A list of dictionaries containing app details with the following keys:
            - id (str): Unique identifier of the app
            - name (str): Name of the app
            - description (str): Description of the app
            - appType (str): Type of the app
            - isPublished (bool): Publication status of the app
            - updateTime (str): Last update timestamp
    """
    apps = appbuilder.get_all_apps()
    return [{
        "id": app.id,
        "name": app.name,
        "description": app.description,
        "appType": app.appType,
        "isPublished": app.isPublished,
        "updateTime": app.updateTime
    } for app in apps]


@server.tool()
def create_conversation(app_id: str) -> str:
    """
    Create a new conversation session for a specific AppBuilder application.

    Args:
        app_id (str): The unique identifier of the target application

    Returns:
        str: A unique conversation identifier that can be used for subsequent interactions

    Example:
        conversation_id = create_conversation("fcc766c4-2bf2-46a3-a63b-1341b05bac49")
    """
    client = appbuilder.AppBuilderClient(app_id)
    conversation_id = client.create_conversation()
    return conversation_id


@server.tool()
def run(app_id: str, conversation_id: str, query: str) -> str:
    """
    Execute a conversation query with a specific AppBuilder application.

    Args:
        app_id (str): The unique identifier of the target application
        conversation_id (str): The conversation session identifier
        query (str): The input text/query to send to the application

    Returns:
        str: The response content from the conversation

    Example:
        response = run_conversation(
            "fcc766c4-2bf2-46a3-a63b-1341b05bac49",
            "conv-123",
            "今天北京天气如何"
        )
    """
    client = appbuilder.AppBuilderClient(app_id)
    output = client.run(conversation_id, query)
    return output.content.answer


if __name__ == "__main__":
    server.run()
