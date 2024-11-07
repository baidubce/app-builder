package com.baidubce.appbuilder.model.knowledgebase;

import java.util.HashMap;
import java.util.Map;

import com.google.gson.annotations.SerializedName;

public class DocumentListRequest {
    @SerializedName("knowledge_base_id")
    private String konwledgeBaseId;
    private int limit;
    private String after;
    private String before;

    // getters and setters
    public String getKonwledgeBaseId() {
        return konwledgeBaseId;
    }

    public void setKonwledgeBaseId(String konwledgeBaseId) {
        this.konwledgeBaseId = konwledgeBaseId;
    }

    public int getLimit() {
        return limit;
    }

    public void setLimit(int limit) {
        this.limit = limit;
    }

    public String getAfter() {
        return after;
    }

    public void setAfter(String after) {
        this.after = after;
    }

    public String getBefore() {
        return before;
    }

    public void setBefore(String before) {
        this.before = before;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("knowledge_base_id", konwledgeBaseId);
        if (limit != 0) {
            map.put("limit", limit);
        }
        map.put("after", after);
        map.put("before", before);
        return map;
    }
}
