package com.baidubce.appbuilder.model.knowledgebase;

public class ChunkModifyRequest {
    private String chunkId;
    private String content;
    private boolean enable;

    public ChunkModifyRequest(String chunkId, String content, boolean enable) {
        this.chunkId = chunkId;
        this.content = content;
        this.enable = enable;
    }

    public String getChunkId() {
        return chunkId;
    }

    public String getContent() {
        return content;
    }

    public boolean getEnable() {
        return enable;
    }
}
