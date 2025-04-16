"""
MCP Server for AI Search.

This module provides an integrated AI search solution that combines Baidu Search capabilities with
Large Language Models (LLMs). It enables Retrieval-Augmented Generation (RAG) workflows by retrieving
relevant information from Baidu Search and using LLMs to generate contextually appropriate responses.
"""

from .ai_search_server import AIsearch, server

__all__ = ["AIsearch", "server"]
