package com.baidubce.appbuilder.model.dataset;

public class DatasetCreateResponse {
    private int code;
    private String message;
    private DatasetCreateResult result;

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

    public DatasetCreateResult getResult() {
        return result;
    }

    public void setResult(DatasetCreateResult result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "DatasetCreateResponse{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", result=" + result +
                '}';
    }
}
