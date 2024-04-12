package com.baidubce.appbuilder.model.rag;

import com.google.gson.annotations.SerializedName;

public class RAGResponse {
    private int code;
    private String message;
    @SerializedName("trace_id")
    private String traceId;
    private long time;
    private RAGResult result;

    public String getTraceId() {
        return traceId;
    }

    public void setTraceId(String traceId) {
        this.traceId = traceId;
    }

    public long getTime() {
        return time;
    }

    public void setTime(int time) {
        this.time = time;
    }

    public RAGResult getResult() {
        return result;
    }

    public void setResult(RAGResult result) {
        this.result = result;
    }

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

    @Override
    public String toString() {
        return "RAGResponse{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", traceId='" + traceId + '\'' +
                ", time=" + time +
                ", result=" + result +
                '}';
    }
}

