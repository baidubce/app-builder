package com.baidubce.appbuilder.model.dataset;

public class FileUploadResponse {
    private int code;
    private String message;
    private FileUploadResult result;

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

    public FileUploadResult getResult() {
        return result;
    }

    public void setResult(FileUploadResult result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "FileUploadResponse{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", result=" + result +
                '}';
    }
}
