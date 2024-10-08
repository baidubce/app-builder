package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class ChunkDeleteRequestTest {

    private ChunkDeleteRequest chunkDeleteRequest;

    @Before
    public void setUp() {
        chunkDeleteRequest = new ChunkDeleteRequest();
    }

    @Test
    public void testSetAndGetChunkId() {
        String expectedChunkId = "chunk123";
        chunkDeleteRequest.setChunkId(expectedChunkId);
        assertEquals(expectedChunkId, chunkDeleteRequest.getChunkId());
    }
}