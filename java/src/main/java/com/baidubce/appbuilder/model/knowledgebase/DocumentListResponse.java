package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class DocumentListResponse {
    @SerializedName("request_id")
    private String requestId;
    private Document[] data;
    private String code;
    private String message;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public Document[] getData() {
        return data;
    }

    public void setData(Document[] data) {
        this.data = data;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
