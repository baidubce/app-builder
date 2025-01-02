package com.baidubce.appbuilder.model.knowledgebase;

public class ChunksDescribeRequest {
    private String knowledgeBaseId;
    private String documentId;
    private String marker;
    private Integer maxKeys;
    private String type;

    public ChunksDescribeRequest(String documentId, String marker, Integer maxKeys, String type) {
        this.documentId = documentId;
        this.marker = marker;
        this.maxKeys = maxKeys;
        this.type = type;
    }

    public ChunksDescribeRequest(String knowledgeBaseId, String documentId, String marker, Integer maxKeys,
            String type) {
        this.knowledgeBaseId = knowledgeBaseId;
        this.documentId = documentId;
        this.marker = marker;
        this.maxKeys = maxKeys;
        this.type = type;
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

    public String getMarker() {
        return marker;
    }

    public void setMarker(String marker) {
        this.marker = marker;
    }

    public Integer getMaxKeys() {
        return maxKeys;
    }

    public void setMaxKeys(Integer maxKeys) {
        this.maxKeys = maxKeys;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
