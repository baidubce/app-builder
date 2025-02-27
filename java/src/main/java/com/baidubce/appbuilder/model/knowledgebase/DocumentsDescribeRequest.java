package com.baidubce.appbuilder.model.knowledgebase;

public class DocumentsDescribeRequest {
    private String knowledgeBaseId;
    private String marker;
    private Integer maxKeys;

    public DocumentsDescribeRequest(String marker, Integer maxKeys) {
        this.marker = marker;
        this.maxKeys = maxKeys;
    }

    public DocumentsDescribeRequest(String knowledgeBaseId, String marker, Integer maxKeys) {
        this.knowledgeBaseId = knowledgeBaseId;
        this.marker = marker;
        this.maxKeys = maxKeys;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
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
}
