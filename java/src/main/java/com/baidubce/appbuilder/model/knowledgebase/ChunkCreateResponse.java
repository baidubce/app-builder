package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class ChunkCreateResponse {
    @SerializedName("id")
    private String chunkId;

    public void setChunkId(String chunkId) {
        this.chunkId = chunkId;
    }

    public String getChunkId() {
        return chunkId;
    }
}
