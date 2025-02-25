package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class KnowledgeBaseModifyRequest {
    @SerializedName("id")
    private String knowledgeBaseId;
    private String name;
    private String description;
    private KnowledgeBaseConfig config;

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public KnowledgeBaseConfig getConfig() {
        return config;
    }

    public void setConfig(KnowledgeBaseConfig config) {
        this.config = config;
    }
}
