package com.baidubce.appbuilder.model.appbuilderclient;

import com.google.gson.annotations.SerializedName;

public class AppBuilderClientFeedbackRequest {
    @SerializedName("app_id")
    private String appId;
    @SerializedName("conversation_id")
    private String conversationId;
    @SerializedName("message_id")
    private String messageId;
    private String type;
    private String[] flag;
    private String reason;

    public AppBuilderClientFeedbackRequest(String appId, String conversationId, String messageId, String type,
            String[] flag, String reason) {
        this.appId = appId;
        this.conversationId = conversationId;
        this.messageId = messageId;
        this.type = type;
        this.flag = flag;
        this.reason = reason;
    }

    public String getAppId() {
        return appId;
    }

    public void setAppId(String appId) {
        this.appId = appId;
    }

    public String getConversationId() {
        return conversationId;
    }

    public void setConversationId(String conversationId) {
        this.conversationId = conversationId;
    }

    public String getMessageId() {
        return messageId;
    }

    public void setMessageId(String messageId) {
        this.messageId = messageId;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String[] getFlag() {
        return flag;
    }

    public void setFlag(String[] flag) {
        this.flag = flag;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }
}
