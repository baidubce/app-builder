package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class DocumentAddRequest {
    @SerializedName("knowledge_base_id")
    private String knowledgeBaseId;
    @SerializedName("content_type")
    private String contentType;
    @SerializedName("is_enhanced")
    private boolean isEnhanced;
    @SerializedName("file_ids")
    private String[] fileIds;
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

    public String[] getFileIds() {
        return fileIds;
    }

    public void setFileIds(String[] fileIds) {
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
        private String[] separators;
        @SerializedName("target_length")
        private int targetLength;
        @SerializedName("overlap_rate")
        private double overlapRate;

        public String[] getSeparators() {
            return separators;
        }

        public void setSeparators(String[] separators) {
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
