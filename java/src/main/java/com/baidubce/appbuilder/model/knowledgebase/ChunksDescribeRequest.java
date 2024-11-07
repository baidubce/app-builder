package com.baidubce.appbuilder.model.knowledgebase;

public class ChunksDescribeRequest {
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

    public String getDocumentId() {
        return documentId;
    }

    public String getMarker() {
        return marker;
    }

    public Integer getMaxKeys() {
        return maxKeys;
    }

    public String getType() {
        return type;
    }
}
