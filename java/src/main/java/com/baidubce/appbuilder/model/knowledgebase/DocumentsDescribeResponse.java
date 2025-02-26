package com.baidubce.appbuilder.model.knowledgebase;

public class DocumentsDescribeResponse {
    private DocumentDescribeResponse[] data;
    private String marker;
    private boolean isTruncated;
    private String nextMarker;
    private Integer maxKeys;

    public DocumentDescribeResponse[] getData() {
        return data;
    }

    public void setData(DocumentDescribeResponse[] data) {
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

    public Integer getMaxKeys() {
        return maxKeys;
    }

    public void setMaxKeys(Integer maxKeys) {
        this.maxKeys = maxKeys;
    }
}
