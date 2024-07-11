package com.baidubce.appbuilder.model.knowledgebase;

public class KnowledgeBaseListRequest {
    // 起始位置
    private String maker;
    // 数据大小，默认10，最大值100
    private int maxKeys;
    // 搜索关键字
    private String keyword;

    public String getMaker() {
        return maker;
    }

    public void setMaker(String maker) {
        this.maker = maker;
    }

    public int getMaxKeys() {
        return maxKeys;
    }

    public void setMaxKeys(int maxKerys) {
        this.maxKeys = maxKerys;
    }

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }
}
