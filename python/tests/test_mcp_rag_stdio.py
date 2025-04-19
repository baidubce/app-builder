# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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

import unittest
import sys
import json
import asyncio
import os
import inspect
import appbuilder
from appbuilder import (
    KnowledgeBase,
)


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestGetAppList(unittest.TestCase):

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_knowledgebase_mcp(self):
        async def process():
            # case list tools
            mcp_client = MCPClient()
            env = {"APPBUILDER_TOKEN": os.getenv("APPBUILDER_TOKEN")}
            await mcp_client.connect_to_server(inspect.getfile(knowledge_base_server), env=env)
            tools = mcp_client.tools
            print(tools)

            # case create_knowledge_base
            result = await mcp_client.call_tool(
                "create_knowledge_base",
                {"name": "mcp测试可删", "description": "mcp测试，可删"},
            )
            knowledge_base_info = json.loads(result.content[0].text)
            knowledge_base_id = knowledge_base_info.get("id")
            assert knowledge_base_id is not None

            # case describe_knowledge_base
            appbuilder.logger.debug(
                f"create knowledge base success: {knowledge_base_id}")
            result = await mcp_client.call_tool(
                "describe_knowledge_base",
                {"id": knowledge_base_id},
            )
            knowledge_base_info = json.loads(result.content[0].text)
            knowledge_base_id = knowledge_base_info.get("id")
            assert knowledge_base_id is not None
            appbuilder.logger.debug(
                f"describe knowledge base success: {knowledge_base_id}"
            )

            # case list_knowledge_bases
            result = await mcp_client.call_tool(
                "list_knowledge_bases",
                {"max_keys": 10},
            )
            assert len(result.content) == 10
            appbuilder.logger.debug(
                f"list knowledge bases success: {len(result.content)}"
            )

            # case upload_document
            result = await mcp_client.call_tool(
                "upload_document",
                {"id": knowledge_base_id,
                    "file_path": "./data/mcp_knowledge_base_case.txt"},
            )
            document_info = json.loads(result.content[0].text)
            print(document_info)
            document_id = document_info.get("documentId")
            assert document_id is not None
            appbuilder.logger.debug(f"upload document success: {document_id}")

            # case list_documents
            result = await mcp_client.call_tool(
                "list_documents",
                {"id": document_id},
            )
            assert len(result.content) == 1
            appbuilder.logger.debug(
                f"list documents base success: {document_id}")

            # case query_knowledge_base
            result = await mcp_client.call_tool(
                "query_knowledge_base",
                {"query": "分子", "id_list": [
                    "56e82915-9642-4a03-bb02-74744c17863e"]},
            )
            assert result.content[0].text is not None
            appbuilder.logger.debug("query knowledge base success")

            await mcp_client.cleanup()

        from appbuilder.mcp_server import MCPClient
        from appbuilder.mcp_server.knowledge_base import knowledge_base_server

        loop = asyncio.get_event_loop()
        loop.run_until_complete(process())


def query_knowledge_base(query: str, id_list: list[str]):
    """
    Query content from KnowledgeBases.

    Args:
        query: Search query string
        id_list: List of KnowledgeBase ID to search in
    """
    client = KnowledgeBase()
    resp = client.query_knowledge_base(query, knowledgebase_ids=id_list)
    return [
        {
            "chunk_id": chunk.chunk_id,
            "content": chunk.content,
            "document_id": chunk.document_id,
            "document_name": chunk.document_name,
        }
        for chunk in resp.chunks
    ]


if __name__ == "__main__":
    appbuilder.logger.setLevel("DEBUG")
    unittest.main()
