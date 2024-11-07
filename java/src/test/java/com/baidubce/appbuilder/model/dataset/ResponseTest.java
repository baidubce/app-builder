package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ResponseTest {
    private DatasetCreateResponse datasetCreateResponse;
    private DocumentAddResponse documentAddResponse;
    private DocumentDeleteResponse documentDeleteResponse;

    @Before
    public void setUp() {
        // Initialize DatasetCreateResponse
        datasetCreateResponse = new DatasetCreateResponse();
        DatasetCreateResult datasetCreateResult = new DatasetCreateResult(); // Assume default constructor
        datasetCreateResponse.setCode(200);
        datasetCreateResponse.setMessage("Dataset created successfully");
        datasetCreateResponse.setResult(datasetCreateResult);

        // Initialize DocumentAddResponse
        documentAddResponse = new DocumentAddResponse();
        DocumentAddResult documentAddResult = new DocumentAddResult(); // Assume default constructor
        documentAddResponse.setCode(201);
        documentAddResponse.setMessage("Document added successfully");
        documentAddResponse.setResult(documentAddResult);

        // Initialize DocumentDeleteResponse
        documentDeleteResponse = new DocumentDeleteResponse();
        documentDeleteResponse.setCode(204);
        documentDeleteResponse.setMessage("Document deleted successfully");
        documentDeleteResponse.setResult(null); // Assume result can be null
    }

    @Test
    public void testDatasetCreateResponse() {
        assertEquals(200, datasetCreateResponse.getCode());
        assertEquals("Dataset created successfully", datasetCreateResponse.getMessage());
        assertNotNull(datasetCreateResponse.getResult());

        String expectedString = "DatasetCreateResponse{" +
                "code=200" +
                ", message='Dataset created successfully'" +
                ", result=" + datasetCreateResponse.getResult() +
                '}';
        assertEquals(expectedString, datasetCreateResponse.toString());
    }

    @Test
    public void testDocumentAddResponse() {
        assertEquals(201, documentAddResponse.getCode());
        assertEquals("Document added successfully", documentAddResponse.getMessage());
        assertNotNull(documentAddResponse.getResult());

        String expectedString = "DocumentAddResponse{" +
                "code=201" +
                ", message='Document added successfully'" +
                ", result=" + documentAddResponse.getResult() +
                '}';
        assertEquals(expectedString, documentAddResponse.toString());
    }

    @Test
    public void testDocumentDeleteResponse() {
        assertEquals(204, documentDeleteResponse.getCode());
        assertEquals("Document deleted successfully", documentDeleteResponse.getMessage());
        assertNull(documentDeleteResponse.getResult());

        String expectedString = "DocumentDeleteResponse{" +
                "code=204" +
                ", message='Document deleted successfully'" +
                ", result=null" +
                '}';
        assertEquals(expectedString, documentDeleteResponse.toString());
    }
}