package com.baidubce.appbuilder.model.rag;

import com.google.gson.annotations.SerializedName;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class EventContent {
    @SerializedName("event_code")
    String eventCode;
    @SerializedName("event_message")
    String enentMessage;
    @SerializedName("node_name")
    String nodeName;
    @SerializedName("dependency_nodes")
    String[] dependencyNodes;
    @SerializedName("event_type")
    String eventType;
    @SerializedName("event_id")
    String eventId;
    @SerializedName("event_status")
    String eventStatus;

    @SerializedName("content_type")
    String contentType;

    Map<String, Object> outputs;

    HashMap<String, String> detail;

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

    public String getNodeName() {
        return nodeName;
    }

    public void setNodeName(String nodeName) {
        this.nodeName = nodeName;
    }

    public String[] getDependencyNodes() {
        return dependencyNodes;
    }

    public void setDependencyNodes(String[] dependencyNodes) {
        this.dependencyNodes = dependencyNodes;
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

    public HashMap<String, String> getDetail() {
        return detail;
    }

    public void setDetail(HashMap<String, String> detail) {
        this.detail = detail;
    }

    @Override
    public String toString() {
        return "EventContent{" +
                "eventCode='" + eventCode + '\'' +
                ", enentMessage='" + enentMessage + '\'' +
                ", nodeName='" + nodeName + '\'' +
                ", dependencyNodes=" + Arrays.toString(dependencyNodes) +
                ", eventType='" + eventType + '\'' +
                ", eventId='" + eventId + '\'' +
                ", eventStatus='" + eventStatus + '\'' +
                ", contentType='" + contentType + '\'' +
                ", outputs=" + outputs +
                ", detail=" + detail +
                '}';
    }
}

