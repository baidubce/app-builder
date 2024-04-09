package com.baidubce.appbuilder.base.exception;

public class AppBuilderServerException extends Exception {
    private String requestId;
    private int code;
    private int appbuilderCode;
    private String appbuilderMessage;

    public AppBuilderServerException(String requestId, int code, String message) {
        super(message); // 调用父类的构造函数，设置异常消息
        this.requestId = requestId;
        this.code = code;
    }

    public AppBuilderServerException(String requestId, int code, String message, int appbuilderCode, String appbuilderMessage) {
        this(requestId, code, message);
        this.appbuilderCode = appbuilderCode;
        this.appbuilderMessage = appbuilderMessage;
    }

    public String getRequestId() {
        return requestId;
    }

    public int getCode() {
        return code;
    }

    @Override
    public String toString() {
        return "AppBuilderServerException{" +
                "requestId='" + requestId + '\'' +
                ", code=" + code +
                ", message=" + getMessage() +
                ", appbuilderCode=" + appbuilderCode +
                ", appbuilderMessage='" + appbuilderMessage + '\'' +
                '}';
    }
}
