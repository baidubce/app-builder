package com.baidubce.appbuilder.base.exception;

public class AppBuilderServerException extends Exception {
    private final String requestId;
    private final int code;
    private final String message;
    private int appbuilderCode;
    private String appbuilderMessage;
    private String responseBody;

    public AppBuilderServerException(String requestId, int code, String message) {
        this.requestId = requestId;
        this.code = code;
        this.message = message;
    }

    public AppBuilderServerException(String requestId, int code, String message, int appbuilderCode, String appbuilderMessage) {
        this(requestId, code, message);
        this.appbuilderCode = appbuilderCode;
        this.appbuilderMessage = appbuilderMessage;
    }

    public AppBuilderServerException(String requestId, int code, String message, String responseBody) {
        this(requestId, code, message);
        this.responseBody = responseBody;
    }

    public String getRequestId() {
        return requestId;
    }

    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public int getAppbuilderCode() {
        return appbuilderCode;
    }

    public String getAppbuilderMessage() {
        return appbuilderMessage;
    }

    public String getResponseBody() {
        return responseBody;
    }

    @Override
    public String toString() {
        return "AppBuilderServerException{" +
                "requestId='" + requestId + '\'' +
                ", code=" + code +
                ", message='" + message + '\'' +
                ", appbuilderCode=" + appbuilderCode +
                ", appbuilderMessage='" + appbuilderMessage + '\'' +
                ", responseBody='" + responseBody + '\'' +
                '}';
    }
}
