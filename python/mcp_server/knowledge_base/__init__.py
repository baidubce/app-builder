"""
MCP Server for Knowledge Base.

This module provides functionality for knowledge base operations.
"""

from .knowledge_base_server import (
    create_knowledge_base,
    query_knowledge_base,
    describe_knowledge_base,
    list_knowledge_bases,
    upload_document,
    list_documents,
    server
)

__all__ = [
    "create_knowledge_base",
    "query_knowledge_base",
    "describe_knowledge_base",
    "list_knowledge_bases",
    "upload_document",
    "list_documents",
    "server"
]
