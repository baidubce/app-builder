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
      "url": "http://appbuilder.baidu.com/v2/knowledge_base/mcp/sse?api_key=Bearer+bce-v3/ALTAK..."
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

### Creating a Knowledge Base

```python
response = create_knowledge_base(
    name="my_knowledge",
    description="my_knowledge"
)
print(response)
```

### Querying a Knowledge Base

```python
response = query_knowledge_base(
    query="民法典第三条",
    id_list=["70c6375a-1595-41f2-9a3b-e81bc9060b7f"]
)
print(response)
```

### Managing Knowledge Base Operations

```python
# Get knowledge base details
response = describe_knowledge_base(
    id="your_knowledge_base_id"
)
print(response)

# List all knowledge bases
response = list_knowledge_bases(max_keys=5)
print(response)

# Upload a document
response = upload_document(
    id="your_knowledge_base_id",
    file_path="path/to/your/document.pdf",
    template="default"
)
print(response)

# List documents in a knowledge base
response = list_documents(
    id="your_knowledge_base_id"
)
print(response)
```
