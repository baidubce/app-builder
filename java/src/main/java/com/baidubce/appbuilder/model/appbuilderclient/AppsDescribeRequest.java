package com.baidubce.appbuilder.model.appbuilderclient;

public class AppsDescribeRequest {
    private String marker;
    private Integer maxKeys;
    
    public AppsDescribeRequest(String marker, Integer maxKeys) {
        this.marker = marker;
        this.maxKeys = maxKeys;
    }

    public AppsDescribeRequest() {
        this.maxKeys = 10;
    }

    public AppsDescribeRequest(Integer maxKeys) {
        this.maxKeys = maxKeys;
    }

    public AppsDescribeRequest(String marker) {
        this.marker = marker;
    }
    
    public String getMarker() {
        return marker;
    }

    public Integer getMaxKeys() {
        return maxKeys;
    }
}
