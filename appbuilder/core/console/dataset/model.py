from typing import List, Optional
from pydantic import BaseModel


class FileInfo(BaseModel):
    id: str
    name: str
    created_from: str
    created_by: str
    created_at: int
    indexing_status: str
    error: Optional[str] = None
    enabled: bool
    disabled_at: Optional[int] = None
    disabled_by: Optional[str] = None
    display_status: str
    word_count: int


class FileListResponse(BaseModel):
    data: List[FileInfo]
    has_more: bool
    limit: int
    total: int
    page: int


class AddFileResponse(BaseModel):
    dataset_id: str
    document_ids: List[str]
