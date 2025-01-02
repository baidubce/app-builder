package com.baidubce.appbuilder.model.knowledgebase;

public class ChunkDeleteRequest {
    private String knowledgeBaseId;
    private String chunkId;

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setChunkId(String chunkId) {
        this.chunkId = chunkId;
    }

    public String getChunkId() {
        return chunkId;
    }
}
