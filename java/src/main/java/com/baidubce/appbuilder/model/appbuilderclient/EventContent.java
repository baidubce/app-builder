package com.baidubce.appbuilder.model.appbuilderclient;

import com.google.gson.annotations.SerializedName;

import java.util.Map;

public class EventContent {
    @SerializedName("event_code")
    private String eventCode;
    @SerializedName("event_message")
    private String enentMessage;
    @SerializedName("event_type")
    private String eventType;
    @SerializedName("event_id")
    private String eventId;
    @SerializedName("event_status")
    private String eventStatus;
    @SerializedName("content_type")
    private String contentType;
    private Map<String, Object> outputs;
    private Map<String, Object> usage;

    public String getEventCode() {
        return eventCode;
    }

    public void setEventCode(String eventCode) {
        this.eventCode = eventCode;
    }

    public String getEnentMessage() {
        return enentMessage;
    }

    public void setEnentMessage(String enentMessage) {
        this.enentMessage = enentMessage;
    }

    public String getEventType() {
        return eventType;
    }

    public void setEventType(String eventType) {
        this.eventType = eventType;
    }

    public String getEventId() {
        return eventId;
    }

    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

    public String getEventStatus() {
        return eventStatus;
    }

    public void setEventStatus(String eventStatus) {
        this.eventStatus = eventStatus;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    public Map<String, Object> getOutputs() {
        return outputs;
    }

    public void setOutputs(Map<String, Object> outputs) {
        this.outputs = outputs;
    }

    public Map<String, Object> getUsage() {
        return usage;
    }

    public void setUsage(Map<String, Object> usage) {
        this.usage = usage;
    }

    @Override
    public String toString() {
        return "EventContent{" +
                "eventCode='" + eventCode + '\'' +
                ", enentMessage='" + enentMessage + '\'' +
                ", eventType='" + eventType + '\'' +
                ", eventId='" + eventId + '\'' +
                ", eventStatus='" + eventStatus + '\'' +
                ", contentType='" + contentType + '\'' +
                ", outputs=" + outputs + '\'' +
                "usage=" + usage + 
                '}';
    }
}
