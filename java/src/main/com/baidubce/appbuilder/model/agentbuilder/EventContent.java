package com.baidubce.appbuilder.model.agentbuilder;

import com.google.gson.annotations.SerializedName;

import java.util.HashMap;
import java.util.Map;

public class EventContent {
    @SerializedName("event_code")
    String eventCode;
    @SerializedName("event_message")
    String enentMessage;
    @SerializedName("event_type")
    String eventType;
    @SerializedName("event_id")
    String eventId;
    @SerializedName("event_status")
    String eventStatus;
    @SerializedName("content_type")
    String contentType;
    Map<String, Object> outputs;

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

    @Override
    public String toString() {
        return "EventContent{" +
                "eventCode='" + eventCode + '\'' +
                ", enentMessage='" + enentMessage + '\'' +
                ", eventType='" + eventType + '\'' +
                ", eventId='" + eventId + '\'' +
                ", eventStatus='" + eventStatus + '\'' +
                ", contentType='" + contentType + '\'' +
                ", outputs=" + outputs +
                '}';
    }
}
