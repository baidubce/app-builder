package com.baidubce.appbuilder.model.appbuilderclient;


import java.util.Arrays;

import com.google.gson.annotations.SerializedName;

public class AppBuilderClientResult {
    private String requestId;
    private String answer;
    @SerializedName("message_id")
    private String messageId;
    private Event[] events;

    public String getAnswer() {
        return answer;
    }

    public AppBuilderClientResult setAnswer(String answer) {
        this.answer = answer;
        return this;
    }

    public String getRequestId() {
        return requestId;
    }

    public AppBuilderClientResult setRequestId(String requestId) {
        this.requestId = requestId;
        return this;
    }

    public String getMessageId() {
        return messageId;
    }

    public AppBuilderClientResult setMessageId(String messageId) {
        this.messageId = messageId;
        return this;
    }

    public Event[] getEvents() {
        return events;
    }

    public AppBuilderClientResult setEvents(Event[] events) {
        this.events = events;
        return this;
    }

    @Override
    public String toString() {
        return "AppBuilderClientResult{" +
                "answer='" + answer + '\'' +
                ", events=" + Arrays.toString(events) +
                '}';
    }
}
