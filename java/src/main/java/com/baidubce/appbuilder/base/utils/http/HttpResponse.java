package com.baidubce.appbuilder.base.utils.http;

import java.util.Map;

public class HttpResponse<T> {
    private int code;
    private String message;
    private String requestId;
    private Map<String, String> headers;

    private T body;

    private String stringBody;

    public int getCode() {
        return code;
    }

    protected HttpResponse<T> setCode(int code) {
        this.code = code;
        return this;
    }

    public String getMessage() {
        return message;
    }

    public HttpResponse<T> setMessage(String message) {
        this.message = message;
        return this;
    }

    public String getRequestId() {
        return requestId;
    }

    public HttpResponse<T> setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }

    public Map<String, String> getHeaders() {
        return headers;
    }

    protected HttpResponse<T> setHeaders(Map<String, String> headers) {
        this.headers = headers;
        return this;
    }

    public T getBody() {
        return body;
    }

    protected HttpResponse<T> setBody(T body) {
        this.body = body;
        return this;
    }

    public String getStringBody() {
        return stringBody;
    }

    protected HttpResponse<T> setStringBody(String stringBody) {
        this.stringBody = stringBody;
        return this;
    }
}