package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ChunkModifyRequestTest {

    private ChunkModifyRequest chunkModifyRequest;

    @Before
    public void setUp() {
        // 初始化 ChunkModifyRequest 对象
        chunkModifyRequest = new ChunkModifyRequest("chunk123", "new content", true);
    }

    @Test
    public void testGetChunkId() {
        assertEquals("chunk123", chunkModifyRequest.getChunkId());
    }

    @Test
    public void testGetContent() {
        assertEquals("new content", chunkModifyRequest.getContent());
    }

    @Test
    public void testGetEnable() {
        assertTrue(chunkModifyRequest.getEnable());
    }
}