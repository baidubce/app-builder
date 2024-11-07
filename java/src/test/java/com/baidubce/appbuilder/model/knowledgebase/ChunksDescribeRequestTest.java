package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ChunksDescribeRequestTest {

    private ChunksDescribeRequest chunksDescribeRequest;

    @Before
    public void setUp() {
        // 初始化 ChunksDescribeRequest 对象
        chunksDescribeRequest = new ChunksDescribeRequest("doc123", "marker123", 10, "chunkType");
    }

    @Test
    public void testGetDocumentId() {
        assertEquals("doc123", chunksDescribeRequest.getDocumentId());
    }

    @Test
    public void testGetMarker() {
        assertEquals("marker123", chunksDescribeRequest.getMarker());
    }

    @Test
    public void testGetMaxKeys() {
        assertEquals(Integer.valueOf(10), chunksDescribeRequest.getMaxKeys());
    }

    @Test
    public void testGetType() {
        assertEquals("chunkType", chunksDescribeRequest.getType());
    }
}