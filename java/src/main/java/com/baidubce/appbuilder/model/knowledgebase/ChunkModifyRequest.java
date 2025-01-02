package com.baidubce.appbuilder.model.knowledgebase;

public class ChunkModifyRequest {
    private String knowledgeBaseId;
    private String chunkId;
    private String content;
    private boolean enable;

    public ChunkModifyRequest(String chunkId, String content, boolean enable) {
        this.chunkId = chunkId;
        this.content = content;
        this.enable = enable;
    }

    public ChunkModifyRequest(String knowledgeBaseId, String chunkId, String content, boolean enable) {
        this.knowledgeBaseId = knowledgeBaseId;
        this.chunkId = chunkId;
        this.content = content;
        this.enable = enable;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getChunkId() {
        return chunkId;
    }

    public void setChunkId(String chunkId) {
        this.chunkId = chunkId;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public boolean getEnable() {
        return enable;
    }

    public void setEnable(boolean enable) {
        this.enable = enable;
    }
}
