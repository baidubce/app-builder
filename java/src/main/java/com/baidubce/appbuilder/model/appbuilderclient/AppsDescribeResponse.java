package com.baidubce.appbuilder.model.appbuilderclient;

public class AppsDescribeResponse {
    private String requestId;
    private String marker;
    private Boolean isTruncated;
    private String nextMarker;
    private Integer maxKeys;
    private App[] data;
    
    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getMarker() {
        return marker;
    }

    public void setMarker(String marker) {
        this.marker = marker;
    }

    public Boolean getIsTruncated() {
        return isTruncated;
    }

    public void setIsTruncated(Boolean isTruncated) {
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

    public App[] getData() {
        return data;
    }

    public void setData(App[] data) {
        this.data = data;
    }
}
