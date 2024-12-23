from typing import List, Optional
from pydantic import BaseModel


class DocumentInfo(BaseModel):
    id: str
    name: str
    created_at: int
    indexing_status: str
    error: Optional[str] = None
    enabled: bool
    disabled_at: Optional[int] = None
    disabled_by: Optional[str] = None
    display_status: str
    word_count: int


class DocumentListResponse(BaseModel):
    data: List[DocumentInfo]
    has_more: bool
    limit: int
    total: int
    page: int


class AddDocumentsResponse(BaseModel):
    dataset_id: str
    document_ids: List[str]
