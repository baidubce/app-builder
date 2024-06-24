package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class FileUploadResponse {
    @SerializedName("request_id")
    private String requestId;
    private String Id;
    private String code;
    private String message;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        Id = id;
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

    @Override
    public String toString() {
        return "FileUploadResponse{" +
                "request_id=" + requestId +
                ", code='" + code + '\'' +
                ", message='" + message +
                '}';
    }
}
