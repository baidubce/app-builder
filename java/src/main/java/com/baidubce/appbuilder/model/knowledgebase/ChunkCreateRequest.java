package com.baidubce.appbuilder.model.knowledgebase;

public class ChunkCreateRequest {
    private String documentId;
    private String content;

    public ChunkCreateRequest(String documetId, String content) {
        this.documentId = documetId;
        this.content = content;
    }

    public String getDocumentId() {
        return documentId;
    }

    public String getContent() {
        return content;
    }
}
