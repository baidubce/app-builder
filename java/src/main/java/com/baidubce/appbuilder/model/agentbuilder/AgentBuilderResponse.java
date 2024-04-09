package com.baidubce.appbuilder.model.agentbuilder;

import com.google.gson.annotations.SerializedName;

import java.util.Arrays;

public class AgentBuilderResponse {
    @SerializedName("request_id")
    private String requestId;
    private String data;
    private String answer;
    @SerializedName("conversation_id")
    private String conversationId;
    @SerializedName("message_id")
    private String messageId;
    @SerializedName("is_completion")
    private boolean isCompletion;
    private EventContent[] content;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
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

    public boolean isCompletion() {
        return isCompletion;
    }

    public void setCompletion(boolean completion) {
        isCompletion = completion;
    }

    public EventContent[] getContent() {
        return content;
    }

    public void setContent(EventContent[] content) {
        this.content = content;
    }

    @Override
    public String toString() {
        return "AgentBuilderResponse{" +
                "requestId='" + requestId + '\'' +
                ", data='" + data + '\'' +
                ", answer='" + answer + '\'' +
                ", conversationId='" + conversationId + '\'' +
                ", messageId='" + messageId + '\'' +
                ", isCompletion=" + isCompletion +
                ", content=" + Arrays.toString(content) +
                '}';
    }
}