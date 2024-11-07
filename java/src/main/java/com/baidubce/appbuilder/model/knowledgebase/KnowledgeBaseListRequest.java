package com.baidubce.appbuilder.model.knowledgebase;

public class KnowledgeBaseListRequest {
    // 起始位置
    private String marker;
    // 数据大小，默认10，最大值100
    private Integer maxKeys;
    // 搜索关键字
    private String keyword;

    public KnowledgeBaseListRequest(String marker, Integer maxKeys, String keyword) {
        this.maxKeys = maxKeys;
        this.marker = marker;
        this.keyword = keyword;
    }

    public String getMarker() {
        return marker;
    }

    public int getMaxKeys() {
        return maxKeys;
    }

    public String getKeyword() {
        return keyword;
    }
}
