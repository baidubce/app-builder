package com.baidubce.appbuilder.model.dataset;

import com.google.gson.annotations.SerializedName;

import java.util.Arrays;

public class DocumentAddResult {
    @SerializedName("dataset_id")
    private String datasetId;
    @SerializedName("document_ids")
    private String[] documentIds;

    public String getDatasetId() {
        return datasetId;
    }

    public void setDatasetId(String datasetId) {
        this.datasetId = datasetId;
    }

    public String[] getDocumentIds() {
        return documentIds;
    }

    public void setDocumentIds(String[] documentIds) {
        this.documentIds = documentIds;
    }

    @Override
    public String toString() {
        return "DocumentAddResult{" +
                "datasetId='" + datasetId + '\'' +
                ", documentIds=" + Arrays.toString(documentIds) +
                '}';
    }
}
