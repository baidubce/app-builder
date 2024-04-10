package com.baidubce.appbuilder.model.rag;

import com.google.gson.annotations.SerializedName;

import java.util.Arrays;

public class RAGResult {
    private String answer;
    @SerializedName("conversation_id")
    private String conversationId;
    @SerializedName("message_id")
    private String messageId;
    @SerializedName("is_completion")
    private Object isCompletion;

    private String prototype;

    private EventContent[] content;

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

    public Object getIsCompletion() {
        return isCompletion;
    }

    public void setIsCompletion(Object isCompletion) {
        this.isCompletion = isCompletion;
    }

    public String getPrototype() {
        return prototype;
    }

    public void setPrototype(String prototype) {
        this.prototype = prototype;
    }

    public EventContent[] getContent() {
        return content;
    }

    public void setContent(EventContent[] content) {
        this.content = content;
    }

    @Override
    public String toString() {
        return "RAGResult{" +
                "answer='" + answer + '\'' +
                ", conversationId='" + conversationId + '\'' +
                ", messageId='" + messageId + '\'' +
                ", isCompletion=" + isCompletion +
                ", prototype='" + prototype + '\'' +
                ", content=" + Arrays.toString(content) +
                '}';
    }
}
