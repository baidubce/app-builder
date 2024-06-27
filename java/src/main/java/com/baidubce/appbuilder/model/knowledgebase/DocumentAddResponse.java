package com.baidubce.appbuilder.model.knowledgebase;

import com.google.gson.annotations.SerializedName;

public class DocumentAddResponse {
    @SerializedName("request_id")
    private String requestId;
    @SerializedName("knowledge_base_id")
    private String knowledgeBaseId;
    @SerializedName("document_ids")
    private String[] documentIds;
    private String code;
    private String message;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getKnowledgeBaseId() {
        return knowledgeBaseId;
    }

    public void setKnowledgeBaseId(String id) {
        this.knowledgeBaseId = id;
    }

    public String[] getDocumentIds() {
        return documentIds;
    }

    public void setDocumentIds(String[] documentIds) {
        this.documentIds = documentIds;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return "FileUploadResponse{" +
                "request_id=" + requestId +
                ", code='" + code + '\'' +
                ", message='" + message +
                '}';
    }
}
