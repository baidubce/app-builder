package com.baidubce.appbuilder.model.appbuilderclient;

import java.util.HashMap;
import java.util.Map;

public class AppListRequest {
    private int limit;
    private String after;
    private String before;

    // getters and setters
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
        if (limit != 0) {
            map.put("limit", limit);
        }
        map.put("after", after);
        map.put("before", before);
        return map;
    }
}