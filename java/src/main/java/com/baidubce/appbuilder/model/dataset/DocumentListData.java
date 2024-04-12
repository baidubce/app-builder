package com.baidubce.appbuilder.model.dataset;

import com.google.gson.annotations.SerializedName;

import java.util.Map;

public class DocumentListData {
    private String id;
    private String name;
    @SerializedName("dataset_process_rule_id")
    private String datasetProcessRuleId;
    @SerializedName("data_source_type")
    private String dataSourceType;
    private int position;
    @SerializedName("data_source_info")
    private Map<String, String> dataSourceInfo;
    @SerializedName("created_from")
    private String createdFrom;
    @SerializedName("created_by")
    private String createdBy;
    @SerializedName("created_at")
    private long createdAt;
    @SerializedName("indexing_status")
    private String indexingStatus;
    private Object error;
    private boolean enabled;
    @SerializedName("display_status")
    private String displayStatus;
    @SerializedName("word_count")
    private int wordCount;
    @SerializedName("estimated_waiting_minutes")
    private int estimatedWaitingMinutes;
    @SerializedName("disabled_at")
    private Object disabledAt;
    @SerializedName("disabled_by")
    private Object disabledBy;

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

    public String getDatasetProcessRuleId() {
        return datasetProcessRuleId;
    }

    public void setDatasetProcessRuleId(String datasetProcessRuleId) {
        this.datasetProcessRuleId = datasetProcessRuleId;
    }

    public String getDataSourceType() {
        return dataSourceType;
    }

    public void setDataSourceType(String dataSourceType) {
        this.dataSourceType = dataSourceType;
    }

    public int getPosition() {
        return position;
    }

    public void setPosition(int position) {
        this.position = position;
    }

    public Map<String, String> getDataSourceInfo() {
        return dataSourceInfo;
    }

    public void setDataSourceInfo(Map<String, String> dataSourceInfo) {
        this.dataSourceInfo = dataSourceInfo;
    }

    public String getCreatedFrom() {
        return createdFrom;
    }

    public void setCreatedFrom(String createdFrom) {
        this.createdFrom = createdFrom;
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

    public String getIndexingStatus() {
        return indexingStatus;
    }

    public void setIndexingStatus(String indexingStatus) {
        this.indexingStatus = indexingStatus;
    }

    public Object getError() {
        return error;
    }

    public void setError(Object error) {
        this.error = error;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getDisplayStatus() {
        return displayStatus;
    }

    public void setDisplayStatus(String displayStatus) {
        this.displayStatus = displayStatus;
    }

    public int getWordCount() {
        return wordCount;
    }

    public void setWordCount(int wordCount) {
        this.wordCount = wordCount;
    }

    public int getEstimatedWaitingMinutes() {
        return estimatedWaitingMinutes;
    }

    public void setEstimatedWaitingMinutes(int estimatedWaitingMinutes) {
        this.estimatedWaitingMinutes = estimatedWaitingMinutes;
    }

    public Object getDisabledAt() {
        return disabledAt;
    }

    public void setDisabledAt(Object disabledAt) {
        this.disabledAt = disabledAt;
    }

    public Object getDisabledBy() {
        return disabledBy;
    }

    public void setDisabledBy(Object disabledBy) {
        this.disabledBy = disabledBy;
    }

    @Override
    public String toString() {
        return "DocumentListData{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", datasetProcessRuleId='" + datasetProcessRuleId + '\'' +
                ", dataSourceType='" + dataSourceType + '\'' +
                ", position=" + position +
                ", dataSourceInfo=" + dataSourceInfo +
                ", createdFrom='" + createdFrom + '\'' +
                ", createdBy='" + createdBy + '\'' +
                ", createdAt=" + createdAt +
                ", indexingStatus='" + indexingStatus + '\'' +
                ", error=" + error +
                ", enabled=" + enabled +
                ", displayStatus='" + displayStatus + '\'' +
                ", wordCount=" + wordCount +
                ", estimatedWaitingMinutes=" + estimatedWaitingMinutes +
                ", disabledAt=" + disabledAt +
                ", disabledBy=" + disabledBy +
                '}';
    }
}