package com.baidubce.appbuilder.model.knowledgebase;

public class KnowledgeBaseListResponse {
    private String requestId;
    private KnowledgeBase[] data;
    private String marker;
    private boolean isTruncated;
    private String nextMarker;
    private int maxKeys;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public KnowledgeBase[] getData() {
        return data;
    }

    public void setData(KnowledgeBase[] data) {
        this.data = data;
    }

    public String getMarker() {
        return marker;
    }

    public void setMarker(String marker) {
        this.marker = marker;
    }

    public boolean isTruncated() {
        return isTruncated;
    }

    public void setTruncated(boolean isTruncated) {
        this.isTruncated = isTruncated;
    }

    public String getNextMarker() {
        return nextMarker;
    }

    public void setNextMarker(String nextMarker) {
        this.nextMarker = nextMarker;
    }

    public int getMaxKeys() {
        return maxKeys;
    }

    public void setMaxKeys(int maxKeys) {
        this.maxKeys = maxKeys;
    }
}
