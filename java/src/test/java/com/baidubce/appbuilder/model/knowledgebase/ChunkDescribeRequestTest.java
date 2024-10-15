package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ChunkDescribeRequestTest {

    private ChunkDescribeRequest chunkDescribeRequest;

    @Before
    public void setUp() {
        // 初始化 ChunkDescribeRequest 对象
        chunkDescribeRequest = new ChunkDescribeRequest();
    }

    @Test
    public void testSetAndGetChunkId() {
        // 设置 chunkId
        chunkDescribeRequest.setChunkId("chunk123");

        // 验证是否正确返回设置的 chunkId
        assertEquals("chunk123", chunkDescribeRequest.getChunkId());
    }
}