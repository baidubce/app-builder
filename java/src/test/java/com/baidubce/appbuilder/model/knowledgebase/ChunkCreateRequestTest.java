package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class ChunkCreateRequestTest {

    private ChunkCreateRequest chunkCreateRequest;

    @Before
    public void setUp() {
        chunkCreateRequest = new ChunkCreateRequest("doc123", "This is the content of the chunk.");
    }

    @Test
    public void testGetDocumentId() {
        assertEquals("doc123", chunkCreateRequest.getDocumentId());
    }

    @Test
    public void testGetContent() {
        assertEquals("This is the content of the chunk.", chunkCreateRequest.getContent());
    }
}