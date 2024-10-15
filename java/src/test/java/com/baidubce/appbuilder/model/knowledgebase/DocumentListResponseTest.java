package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DocumentListResponseTest {
    private DocumentListResponse documentListResponse;
    private Document document1;
    private Document document2;

    @Before
    public void setUp() {
        documentListResponse = new DocumentListResponse();

        // Initialize Document objects (assuming Document has default constructor and setters)
        document1 = new Document();
        document1.setId("doc1");
        document1.setName("Document 1");

        document2 = new Document();
        document2.setId("doc2");
        document2.setName("Document 2");

        documentListResponse.setRequestId("testRequestId");
        documentListResponse.setData(new Document[]{document1, document2});
        documentListResponse.setCode("200");
        documentListResponse.setMessage("Request successful");
    }

    @Test
    public void testRequestId() {
        assertEquals("testRequestId", documentListResponse.getRequestId());
    }

    @Test
    public void testData() {
        Document[] data = documentListResponse.getData();
        assertNotNull(data);
        assertEquals(2, data.length);
        assertEquals("doc1", data[0].getId());
        assertEquals("Document 1", data[0].getName());
        assertEquals("doc2", data[1].getId());
        assertEquals("Document 2", data[1].getName());
    }

    @Test
    public void testCode() {
        assertEquals("200", documentListResponse.getCode());
    }

    @Test
    public void testMessage() {
        assertEquals("Request successful", documentListResponse.getMessage());
    }
}