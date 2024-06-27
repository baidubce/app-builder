package com.baidubce.appbuilder.model.knowledgebase;

import java.util.HashMap;
import java.util.Map;

import com.google.gson.annotations.SerializedName;

public class DocumentDeleteRequest {
    @SerializedName("knowledge_base_id")
    private String konwledgeBaseId;
    @SerializedName("document_id")
    private String documentId;

    // getters and setters
    public String getKonwledgeBaseId() {
        return konwledgeBaseId;
    }

    public void setKonwledgeBaseId(String konwledgeBaseId) {
        this.konwledgeBaseId = konwledgeBaseId;
    }

    public String getDocumentId() {
        return documentId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("knowledge_base_id", konwledgeBaseId);
        map.put("document_id", documentId);
        return map;
    }
}
