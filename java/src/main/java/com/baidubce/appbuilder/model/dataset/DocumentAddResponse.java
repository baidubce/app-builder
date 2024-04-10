package com.baidubce.appbuilder.model.dataset;

public class DocumentAddResponse {
    private int code;
    private String message;
    private DocumentAddResult result;

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

    public DocumentAddResult getResult() {
        return result;
    }

    public void setResult(DocumentAddResult result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "DocumentAddResponse{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", result=" + result +
                '}';
    }
}
