package com.baidubce.appbuilder.model.agentbuilder;

import com.google.gson.annotations.SerializedName;

public class ConversationResult {
    @SerializedName("conversation_id")
    private String conversationId;

    public String getConversationId() {
        return conversationId;
    }

    public void setConversationId(String conversationId) {
        this.conversationId = conversationId;
    }

    @Override
    public String toString() {
        return "ConversationResult{" +
                "conversationId='" + conversationId + '\'' +
                '}';
    }
}
