package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ChunkCreateResponseTest {

    private ChunkCreateResponse chunkCreateResponse;

    @Before
    public void setUp() {
        // 初始化 ChunkCreateResponse 对象
        chunkCreateResponse = new ChunkCreateResponse();
    }

    @Test
    public void testSetAndGetChunkId() {
        // 设置 chunkId
        chunkCreateResponse.setChunkId("chunk123");

        // 验证是否正确返回设置的 chunkId
        assertEquals("chunk123", chunkCreateResponse.getChunkId());
    }
}