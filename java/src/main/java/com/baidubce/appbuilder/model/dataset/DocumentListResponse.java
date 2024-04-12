package com.baidubce.appbuilder.model.dataset;

public class DocumentListResponse {
    private int code;
    private String message;
    private DocumentListResult result;

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public DocumentListResult getResult() {
        return result;
    }

    public void setResult(DocumentListResult result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "DocumentListResponse{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", result=" + result +
                '}';
    }
}
