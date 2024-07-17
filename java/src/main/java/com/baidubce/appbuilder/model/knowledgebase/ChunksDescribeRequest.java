package com.baidubce.appbuilder.model.knowledgebase;

public class ChunksDescribeRequest {
    private String documentId;
    private String marker;
    private Integer maxKeys;
    private Integer type;

    public ChunksDescribeRequest(String documentId, String marker, Integer maxKeys, Integer type) {
        this.documentId = documentId;
        this.marker = marker;
        this.maxKeys = maxKeys;
        this.type = type;
    }

    public String getDocumentId() {
        return documentId;
    }

    public String getMarker() {
        return marker;
    }

    public Integer getMaxKeys() {
        return maxKeys;
    }

    public Integer getType() {
        return type;
    }
}
