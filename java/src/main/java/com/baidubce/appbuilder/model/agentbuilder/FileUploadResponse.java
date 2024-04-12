package com.baidubce.appbuilder.model.agentbuilder;

import com.google.gson.annotations.SerializedName;

public class FileUploadResponse {
    private String requestId;
    @SerializedName("id")
    private String fileId;
    @SerializedName("conversation_id")
    private String conversationId;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getFileId() {
        return fileId;
    }

    @Override
    public String toString() {
        return "FileUploadResponse{" +
                "requestId='" + requestId + '\'' +
                ", fileId='" + fileId + '\'' +
                ", conversationId='" + conversationId + '\'' +
                '}';
    }

    public void setFileId(String fileId) {
        this.fileId = fileId;
    }

    public String getConversationId() {
        return conversationId;
    }

    public void setConversationId(String conversationId) {
        this.conversationId = conversationId;
    }
}
