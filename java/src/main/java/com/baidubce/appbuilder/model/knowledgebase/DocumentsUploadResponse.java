package com.baidubce.appbuilder.model.knowledgebase;

public class DocumentsUploadResponse {
    private String requestId;
    private String documentId;

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getDocumentId() {
        return documentId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }
}