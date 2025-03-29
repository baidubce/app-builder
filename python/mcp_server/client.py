# Based on https://modelcontextprotocol.io/quickstart/client
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from appbuilder.utils.logger_util import logger


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools = None
        self.sessions = {}
        self.tool_to_server = {}
        self._session_context = None
        self._streams_context = None

    async def connect_to_server(
        self, server_script_path: str = None, service_url: str = None, env: dict = None
    ):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
            service_url: URL of the service
        """
        if server_script_path is not None:
            await self._connect_to_stdio_server(server_script_path, env=env)
        elif service_url is not None:
            await self._connect_to_sse_server(service_url)
        else:
            raise ValueError(
                "Either server_script_path or service_url must be provided."
            )

    async def _connect_to_stdio_server(self, server_script_path: str, env: dict = None):
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = sys.executable if is_python else "node"
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=env
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()
        response = await self.session.list_tools()
        tools = response.tools
        self.tools = tools
        logger.info(
            "\nConnected to server with tools:" +
            str([tool.name for tool in tools])
        )
        cmd_key = f"{command} {' '.join(server_script_path)}"
        self._store_session_and_tools(cmd_key)

    async def _connect_to_sse_server(self, service_url: str):
        self._streams_context = sse_client(url=service_url)
        streams = await self._streams_context.__aenter__()
        self._session_context = ClientSession(*streams)
        self.session: ClientSession = await self._session_context.__aenter__()
        await self.session.initialize()
        response = await self.session.list_tools()
        tools = response.tools
        self.tools = tools
        logger.info(
            "\nConnected to server with tools:" +
            str([tool.name for tool in tools])
        )
        self._store_session_and_tools(service_url)

    def _store_session_and_tools(self, cmd_key):
        new_sessions = {cmd_key: self.session}
        new_sessions.update(self.sessions)
        self.sessions = new_sessions
        for tool in self.tools:
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
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)
