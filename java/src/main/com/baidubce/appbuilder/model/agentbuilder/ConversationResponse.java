package com.baidubce.appbuilder.model.agentbuilder;

public class ConversationResponse {
    private String requestId;
    private int code;
    private String message;
    private ConversationResult result;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
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

    public ConversationResult getResult() {
        return result;
    }

    public void setResult(ConversationResult result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "ConversationResponse{" +
                "requestId='" + requestId + '\'' +
                ", code=" + code +
                ", message='" + message + '\'' +
                ", result=" + result +
                '}';
    }
}
