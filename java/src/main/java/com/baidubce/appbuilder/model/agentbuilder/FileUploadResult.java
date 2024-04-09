package com.baidubce.appbuilder.model.agentbuilder;

import com.google.gson.annotations.SerializedName;

public class FileUploadResult {
    @SerializedName("id")
    private String fileId;
    @SerializedName("conversation_id")
    private String conversationId;

    public String getFileId() {
        return fileId;
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

    @Override
    public String toString() {
        return "FileUploadResult{" +
                "fileId='" + fileId + '\'' +
                ", conversationId='" + conversationId + '\'' +
                '}';
    }
}
