package com.baidubce.appbuilder.model.appbuilderclient;

import com.google.gson.annotations.SerializedName;

public class ConversationResponse {
    private String requestId;

    @SerializedName("conversation_id")
    private String conversationId;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getConversationId() {
        return conversationId;
    }

    public void setConversationId(String conversationId) {
        this.conversationId = conversationId;
    }

    @Override
    public String toString() {
        return "ConversationResponse{" +
                "requestId='" + requestId + '\'' +
                ", conversationId='" + conversationId + '\'' +
                '}';
    }
}
