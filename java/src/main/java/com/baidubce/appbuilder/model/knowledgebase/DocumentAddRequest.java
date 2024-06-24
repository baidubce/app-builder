package com.baidubce.appbuilder.model.knowledgebase;

import java.util.List;

import com.google.gson.annotations.SerializedName;

public class DocumentAddRequest {
   @SerializedName("knowledge_base_id")
    private String knowledgeBaseId;
    @SerializedName("content_type")
    private String contentType;
    @SerializedName("is_enhanced")
    private boolean isEnhanced;
    @SerializedName("file_ids")
    private List<String> fileIds;
    @SerializedName("custom_process_rule")
    private CustomProcessRule customProcessRule;

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setKnowledgeBaseId(String knowledgeBaseId) {
        this.knowledgeBaseId = knowledgeBaseId;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    public boolean isEnhanced() {
        return isEnhanced;
    }

    public void setEnhanced(boolean enhanced) {
        isEnhanced = enhanced;
    }

    public List<String> getFileIds() {
        return fileIds;
    }

    public void setFileIds(List<String> fileIds) {
        this.fileIds = fileIds;
    }

    public CustomProcessRule getCustomProcessRule() {
        return customProcessRule;
    }

    public void setCustomProcessRule(CustomProcessRule customProcessRule) {
        this.customProcessRule = customProcessRule;
    }

    public static class CustomProcessRule {
        @SerializedName("separators")
        private List<String> separators;
        @SerializedName("target_length")
        private int targetLength;
        @SerializedName("overlap_rate")
        private double overlapRate;

        public List<String> getSeparators() {
            return separators;
        }

        public void setSeparators(List<String> separators) {
            this.separators = separators;
        }

        public int getTargetLength() {
            return targetLength;
        }

        public void setTargetLength(int targetLength) {
            this.targetLength = targetLength;
        }

        public double getOverlapRate() {
            return overlapRate;
        }

        public void setOverlapRate(double overlapRate) {
            this.overlapRate = overlapRate;
        }
    }
}
