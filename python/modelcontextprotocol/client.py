# Based on https://modelcontextprotocol.io/quickstart/client
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from appbuilder.utils.logger_util import logger

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools = None
        self.sessions={}
        self.tool_to_server = {}

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = sys.executable if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
        response = await self.session.list_tools()
        tools = response.tools
        self.tools = tools
        logger.info(
            "\nConnected to server with tools:" +
            str([tool.name for tool in tools])
        )

        # Store session with its command as key
        cmd_key = f"{command} {' '.join(server_script_path)}"

        # Store the new session first
        new_sessions = {cmd_key: self.session}
        new_sessions.update(self.sessions)
        self.sessions = new_sessions
        for tool in tools:
            if tool.name in self.tool_to_server:
                raise ValueError(f"Duplicate tool name: {tool.name}")
            self.tool_to_server[tool.name] = cmd_key

    async def call_tool(self, tool_name, tool_args):
        server_cmd = self.tool_to_server.get(tool_name)
        if server_cmd is None:
            raise ValueError(f"Tool '{tool_name}' not found")
        session = self.sessions[server_cmd]
        result = await session.call_tool(name=tool_name, arguments=tool_args)
        return result

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
