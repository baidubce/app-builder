package com.baidubce.appbuilder.model.knowledgebase;

public class ChunkCreateRequest {
    private String knowledgeBaseId;
    private String documentId;
    private String content;


    public ChunkCreateRequest(String documetId, String content) {
        this.documentId = documetId;
        this.content = content;
    }

    public ChunkCreateRequest(String knowledgeBaseId, String documetId, String content) {
        this.knowledgeBaseId = knowledgeBaseId;
        this.documentId = documetId;
        this.content = content;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getDocumentId() {
        return documentId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}
