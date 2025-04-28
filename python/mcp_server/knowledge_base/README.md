# Knowledge Base MCP Server

Knowledge Base MCP Server provides a set of tools for managing knowledge bases and documents through the MCP protocol. It allows you to create, query, and manage knowledge bases and their contents.

## Features

* **Knowledge Base Creation and Management**: Create new knowledge bases and list all available knowledge bases.
* **Document Management**: Upload files to knowledge bases and list all documents in a knowledge base.
* **Knowledge Base Querying**: Search knowledge bases with query strings.

## Quick Start

1. Get your AppBuilder API Key from the console
2. Format your authorization token as: `Bearer+<AppBuilder API Key>` (keep the "+" in between)
3. Config with

```json
{
  "mcpServers": {
    "knowledge_base": {
      "url": "http://appbuilder.baidu.com/v2/knowledgeBase/mcp/sse?api_key=Bearer+bce-v3/ALTAK..."
    }
  }
}
```

## Available Tools

### create_knowledge_base

Creates a new knowledge base.

**Parameters:**
- `name` (str): Name of the KnowledgeBase.
- `description` (str): Description of the KnowledgeBase.

**Returns:**
- Dictionary containing the knowledge base ID, name, description, and request ID.

### describe_knowledge_base

Get details of a specific KnowledgeBase.

**Parameters:**
- `id` (str): ID of the KnowledgeBase.

**Returns:**
- Dictionary containing the knowledge base ID, name, and description.

### list_knowledge_bases

List all KnowledgeBases.

**Parameters:**
- `max_keys` (int, optional): Maximum number of KnowledgeBases to return. Default is 10.

**Returns:**
- List of dictionaries, each containing a knowledge base's ID, name, and description.

### query_knowledge_base

Query content from KnowledgeBases.

**Parameters:**
- `query` (str): Search query string.
- `id_list` (list[str]): List of KnowledgeBase IDs to search in.

**Returns:**
- List of dictionaries, each containing a chunk's ID, content, document ID, and document name.

### upload_document

Upload documents to a KnowledgeBase.

**Parameters:**
- `id` (str): KnowledgeBase ID.
- `file_path` (str): Path to the file to upload.
- `template` (str, optional): Optional processing template to use. Options: "ppt", "paper", "resume", or "default". Default is "default".

**Returns:**
- Dictionary containing the document ID and request ID.

### list_documents

Get all documents in a KnowledgeBase.

**Parameters:**
- `id` (str): Knowledge base ID.

**Returns:**
- List of dictionaries, each containing a document's ID, name, and word count.

## Usage Examples

```python
import asyncio
import json
import io
import os
import appbuilder
from appbuilder.mcp_server.client import MCPClient

os.environ["APPBUILDER_TOKEN"] = "YOUR_APPBUILDER_TOKEN"

async def main():
    mcp_client = MCPClient()
    await mcp_client.connect_to_server(service_url=service_url)

    # case create_knowledge_base
    result = await mcp_client.call_tool(
        "create_knowledge_base",
        {"name": "mcp测试可删", "description": "mcp测试，可删"},
    )
    knowledge_base_info = json.loads(result.content[0].text)
    knowledge_base_id = knowledge_base_info.get("id")
    assert knowledge_base_id is not None

    # case describe_knowledge_base
    appbuilder.logger.debug(f"create knowledge base success: {knowledge_base_id}")
    result = await mcp_client.call_tool(
        "describe_knowledge_base",
        {"id": knowledge_base_id},
    )
    knowledge_base_info = json.loads(result.content[0].text)
    knowledge_base_id = knowledge_base_info.get("id")
    assert knowledge_base_id is not None
    appbuilder.logger.debug(f"describe knowledge base success: {knowledge_base_id}")

    # case list_knowledge_bases
    result = await mcp_client.call_tool(
        "list_knowledge_bases",
        {"max_keys": 10},
    )
    assert len(result.content) == 10
    appbuilder.logger.debug(f"list knowledge bases success: {len(result.content)}")

    # case upload_document
    file_content = "这里是你的文件内容字符串"
    with io.BytesIO(file_content.encode("utf-8")) as f:
        result = await mcp_client.call_tool(
            "upload_document",
            {"id": knowledge_base_id, "file_data": f, "file_name": "test.txt"},
        )
    document_info = json.loads(result.content[0].text)

    document_id = document_info.get("documentId")
    assert document_id is not None
    appbuilder.logger.debug(f"upload document success: {document_id}")

    # case list_documents
    result = await mcp_client.call_tool(
        "list_documents",
        {"id": knowledge_base_id},
    )
    print(result)
    appbuilder.logger.debug(f"list documents base success: {knowledge_base_id}")

    # case query_knowledge_base
    result = await mcp_client.call_tool(
        "query_knowledge_base",
        {"query": "分子", "id_list": [knowledge_base_id]},
    )
    assert result.content[0].text is not None
    appbuilder.logger.debug("query knowledge base success")


if __name__ == "__main__":
    service_url = (
        "http://appbuilder.baidu.com/v2/ai_search/mcp/sse?api_key="
        + os.environ.get("APPBUILDER_TOKEN")
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
