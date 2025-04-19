"""
Baidu AI Search MCP Server stdio server file.
We also support access via SSE protocol. The access address is:
http://appbuilder.baidu.com/v2/ai_search/mcp/sse?api_key=<your api_key>
You can refer to this webpage https://cloud.baidu.com/doc/AppBuilder/s/klv2eywua to obtain the api_key, in the format of "Bearer+bce…".
"""

from enum import Enum
from typing import Literal

from mcp.server import FastMCP
from appbuilder import KnowledgeBase, DocumentProcessOption, DocumentChoices

class TemplateType(str, Enum):
    PPT = "ppt"
    PAPER = "paper"
    RESUME = "resume"
    CUSTOM = "custom"
    DEFAULT = "default"
    QA_PAIR = "qaPair"

class ParserChoices(str, Enum):
    LAYOUT_ANALYSIS = "layoutAnalysis"
    OCR = "ocr"
    PAGE_IMAGE_ANALYSIS = "pageImageAnalysis"
    CHART_ANALYSIS = "chartAnalysis"
    TABLE_ANALYSIS = "tableAnalysis"

server = FastMCP(name="AppBuilder KnowledgeBase MCP Server")

@server.tool()
def create_knowledge_base(name: str, description: str):
    """
    Create a new KnowledgeBase.
    
    Args:
        name: Name of the KnowledgeBase
        description: Description of the KnowledgeBase
    """
    client = KnowledgeBase()
    kb = client.create_knowledge_base(name=name, description=description, type="public")
    return {
        "id": kb.id,
        "name": kb.name,
        "description": kb.description,
        "requestId": kb.requestId
    }

@server.tool()
def describe_knowledge_base(id: str):
    """
    Get details of a specific KnowledgeBase.
    
    Args:
        id: ID of the KnowledgeBase
    """
    client = KnowledgeBase()
    kb = client.get_knowledge_base_detail(id)
    return {
        "id": kb.id,
        "name": kb.name,
        "description": kb.description
    }

@server.tool()
def list_knowledge_bases(max_keys: int = 10):
    """
    List all KnowledgeBase.
    
    Args:
        max_keys: Maximum number of KnowledgeBase to return (default: 10)
    """
    client = KnowledgeBase()
    resp = client.get_knowledge_base_list(maxKeys=max_keys)
    return [{
        "id": kb.id,
        "name": kb.name,
        "description": kb.description
    } for kb in resp.data]

@server.tool()
def query_knowledge_base(query: str, id_list: list[str]):
    """
    Query content from KnowledgeBases.
    
    Args:
        query: Search query string
        id_list: List of KnowledgeBase ID to search in
    """
    client = KnowledgeBase()
    resp = client.query_knowledge_base(query, knowledgebase_ids=id_list)
    return [{
        "chunk_id": chunk.chunk_id,
        "content": chunk.content,
        "document_id": chunk.document_id,
        "document_name": chunk.document_name
    } for chunk in resp.chunks]

@server.tool()
def upload_document(
    id: str, 
    file_path: str, 
    template: Literal["ppt", "paper", "resume", "default"] = "default",
    ):
    """
    Upload documents to a KnowledgeBase.
    
    Args:
        id: KnowledgeBase ID
        file_path: Path to the file to upload
        template: Optional processing template to use. Options:
            - ppt: PPT slides
            - paper: Academic papers
            - resume: Resume documents
            - default: Default configuration
    """
    if template not in TemplateType.__members__.values():
        raise ValueError(f"Invalid template. Must be one of: {list(TemplateType.__members__.values())}")

    content_format: str = "rawText"
    option = DocumentProcessOption(template=template)
    option.parser = DocumentChoices(choices=["layoutAnalysis", "ocr", "pageImageAnalysis", "chartAnalysis", "tableAnalysis"])

    client = KnowledgeBase()
    resp = client.upload_documents(
        id=id,
        content_format=content_format,
        file_path=file_path,
        processOption=option
    )
    
    return {
        "documentId": resp.documentId,
        "requestId": resp.requestId
    }

@server.tool()
def list_documents(id: str):
    """
    Get all documents in a KnowledgeBase.
    
    Args:
        id: Knowledge base ID
    """
    client = KnowledgeBase()
    resp = client.get_all_documents(id)
    return [{
        "id": doc.id,
        "name": doc.name,
        "word_count": doc.word_count
    } for doc in resp]

if __name__ == "__main__":
    server.run()
