package com.baidubce.appbuilder.model.knowledgebase;

public class KnowledgeBase {
    private String id;
    private String name;
    private String description;
    private KnowledgeBaseConfig config;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public KnowledgeBaseConfig getConfig() {
        return config;
    }

    public void setConfig(KnowledgeBaseConfig config) {
        this.config = config;
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
}
