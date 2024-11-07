package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class ChunkDescribeResponse {
    @SerializedName("id")
    private String chunkId;
    private String type;
    private String knowledgeBaseId;
    private String documentId;
    private String content;
    private Integer wordCount;
    private Integer tokenCount;
    private boolean enabled;
    private String status;
    private String statusMessage;
    private String[] imageUrls;
    private Integer createTime;
    private Integer updateTime;

    public void setChunkId(String chunkId) {
        this.chunkId = chunkId;
    }

    public String getChunkId() {
        return chunkId;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getType() {
        return type;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }

    public String getDocumentId() {
        return documentId;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getContent() {
        return content;
    }

    public void setWordCount(Integer wordCount) {
        this.wordCount = wordCount;
    }

    public Integer getWordCount() {
        return wordCount;
    }

    public void setTokenCount(Integer tokenCount) {
        this.tokenCount = tokenCount;
    }

    public Integer getTokenCount() {
        return tokenCount;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public boolean getEnabled() {
        return enabled;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getStatus() {
        return status;
    }

    public void setStatusMessage(String statusMessage) {
        this.statusMessage = statusMessage;
    }

    public String getStatusMessage() {
        return statusMessage;
    }

    public void setImageUrls(String[] imageUrls) {
        this.imageUrls = imageUrls;
    }

    public String[] getImageUrls() {
        return imageUrls;
    }

    public void setCreateTime(Integer createTime) {
        this.createTime = createTime;
    }

    public Integer getCreateTime() {
        return createTime;
    }

    public void setUpdateTime(Integer updateTime) {
        this.updateTime = updateTime;
    }

    public Integer getUpdateTime() {
        return updateTime;
    }
}
