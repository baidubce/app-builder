package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DocumentListResponseTest {
    private DocumentListResponse documentListResponse;
    private DocumentListResult documentListResult;

    @Before
    public void setUp() {
        documentListResponse = new DocumentListResponse();

        // Initialize DocumentListResult (assuming it has a default constructor and setters)
        documentListResult = new DocumentListResult();
        documentListResult.setTotal(100);
        documentListResult.setPage(1);
    }

    @Test
    public void testCode() {
        documentListResponse.setCode(200);
        assertEquals(200, documentListResponse.getCode());
    }

    @Test
    public void testMessage() {
        documentListResponse.setMessage("Request successful");
        assertEquals("Request successful", documentListResponse.getMessage());
    }

    @Test
    public void testResult() {
        documentListResponse.setResult(documentListResult);
        assertNotNull(documentListResponse.getResult());
        assertEquals(100, documentListResponse.getResult().getTotal());
        assertEquals(1, documentListResponse.getResult().getPage());
    }

    @Test
    public void testToString() {
        documentListResponse.setCode(200);
        documentListResponse.setMessage("Request successful");
        documentListResponse.setResult(documentListResult);

        String expectedString = "DocumentListResponse{" +
                "code=200, message='Request successful', result=" + documentListResult + "}";
        assertEquals(expectedString, documentListResponse.toString());
    }
}