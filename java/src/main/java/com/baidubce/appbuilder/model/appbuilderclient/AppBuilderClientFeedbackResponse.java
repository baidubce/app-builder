package com.baidubce.appbuilder.model.appbuilderclient;

import com.google.gson.annotations.SerializedName;

public class AppBuilderClientFeedbackResponse {
    @SerializedName("request_id")
    private String requestId;
    private String code;
    private String message;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
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
