package com.baidubce.appbuilder.model.knowledgebase;

public class ChunkDescribeRequest {
    private String knowledgeBaseId;
    private String chunkId;

    public void setChunkId(String chunkId) {
        this.chunkId = chunkId;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getChunkId() {
        return chunkId;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }
}
