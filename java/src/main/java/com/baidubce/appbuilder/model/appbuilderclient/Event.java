package com.baidubce.appbuilder.model.appbuilderclient;

import java.util.Map;

public class Event {
    private String code;
    private String message;
    private String eventType;
    private String status;
    private String contentType;
    private Map<String, Object> detail;
    private Map<String, Object> usage;

    public String getCode() {
        return code;
    }

    public Event setCode(String code) {
        this.code = code;
        return this;
    }

    public String getMessage() {
        return message;
    }

    public Event setMessage(String message) {
        this.message = message;
        return this;
    }

    public String getEventType() {
        return eventType;
    }

    public Event setEventType(String eventType) {
        this.eventType = eventType;
        return this;
    }

    public String getStatus() {
        return status;
    }

    public Event setStatus(String status) {
        this.status = status;
        return this;
    }

    public String getContentType() {
        return contentType;
    }

    public Event setContentType(String contentType) {
        this.contentType = contentType;
        return this;
    }

    public Map<String, Object> getDetail() {
        return detail;
    }

    public Event setDetail(Map<String, Object> detail) {
        this.detail = detail;
        return this;
    }

    public Map<String, Object> getUsage() {
        return usage;
    }

    public Event setUsage(Map<String, Object> usage) {
        this.usage = usage;
        return this;
    }

    @Override
    public String toString() {
        return "Event{" +
                "code='" + code + '\'' +
                ", message='" + message + '\'' +
                ", eventType='" + eventType + '\'' +
                ", status='" + status + '\'' +
                ", contentType='" + contentType + '\'' +
                ", detail=" + detail + '\'' +
                ", usage=" + usage +
                '}';
    }
}
