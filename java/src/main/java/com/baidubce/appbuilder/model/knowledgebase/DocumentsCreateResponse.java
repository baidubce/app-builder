package com.baidubce.appbuilder.model.knowledgebase;

public class DocumentsCreateResponse {
    private String requestId;
    private String[] documentIds;
    public String getRequestId() {
        return requestId;
    }
    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }
    public String[] getDocumentIds() {
        return documentIds;
    }
    public void setDocumentIds(String[] documentIds) {
        this.documentIds = documentIds;
    }
}
