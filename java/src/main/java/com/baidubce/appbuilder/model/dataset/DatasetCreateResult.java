package com.baidubce.appbuilder.model.dataset;

import com.google.gson.annotations.SerializedName;

public class DatasetCreateResult {
    private String id;
    private String name;
    private String description;
    @SerializedName("indexing_technique")
    private String indexingTechnique;
    @SerializedName("document_count")
    private int documentCount;
    @SerializedName("word_count")
    private int wordCount;
    @SerializedName("created_by")
    private String createdBy;
    @SerializedName("created_at")
    private long createdAt;
    @SerializedName("updated_by")
    private String updatedBy;
    @SerializedName("updated_at")
    private long updatedAt;
    @SerializedName("is_priority")
    private boolean isPriority;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
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

    public String getIndexingTechnique() {
        return indexingTechnique;
    }

    public void setIndexingTechnique(String indexingTechnique) {
        this.indexingTechnique = indexingTechnique;
    }

    public int getDocumentCount() {
        return documentCount;
    }

    public void setDocumentCount(int documentCount) {
        this.documentCount = documentCount;
    }

    public int getWordCount() {
        return wordCount;
    }

    public void setWordCount(int wordCount) {
        this.wordCount = wordCount;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public long getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(long createdAt) {
        this.createdAt = createdAt;
    }

    public String getUpdatedBy() {
        return updatedBy;
    }

    public void setUpdatedBy(String updatedBy) {
        this.updatedBy = updatedBy;
    }

    public long getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(long updatedAt) {
        this.updatedAt = updatedAt;
    }

    public boolean isPriority() {
        return isPriority;
    }

    public void setPriority(boolean priority) {
        isPriority = priority;
    }

    @Override
    public String toString() {
        return "DatasetCreateResult{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", description='" + description + '\'' +
                ", indexingTechnique='" + indexingTechnique + '\'' +
                ", documentCount=" + documentCount +
                ", wordCount=" + wordCount +
                ", createdBy='" + createdBy + '\'' +
                ", createdAt=" + createdAt +
                ", updatedBy='" + updatedBy + '\'' +
                ", updatedAt=" + updatedAt +
                ", isPriority=" + isPriority +
                '}';
    }
}
