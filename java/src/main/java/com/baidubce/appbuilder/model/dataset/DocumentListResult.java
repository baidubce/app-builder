package com.baidubce.appbuilder.model.dataset;

import com.google.gson.annotations.SerializedName;

import java.util.Arrays;

public class DocumentListResult {
    @SerializedName("has_more")
    private boolean hasMore;
    private int limit;
    private int page;
    private int total;
    private DocumentListData[] data;

    public boolean isHasMore() {
        return hasMore;
    }

    public void setHasMore(boolean hasMore) {
        this.hasMore = hasMore;
    }

    public int getLimit() {
        return limit;
    }

    public void setLimit(int limit) {
        this.limit = limit;
    }

    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }

    public DocumentListData[] getData() {
        return data;
    }

    public void setData(DocumentListData[] data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "DocumentListResult{" +
                "hasMore=" + hasMore +
                ", limit=" + limit +
                ", page=" + page +
                ", total=" + total +
                ", data=" + Arrays.toString(data) +
                '}';
    }
}