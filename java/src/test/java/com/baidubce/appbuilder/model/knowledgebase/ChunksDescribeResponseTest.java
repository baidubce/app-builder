package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ChunksDescribeResponseTest {
    private ChunksDescribeResponse chunksDescribeResponse;
    private ChunkDescribeResponse chunk1;
    private ChunkDescribeResponse chunk2;

    @Before
    public void setUp() {
        chunksDescribeResponse = new ChunksDescribeResponse();

        // Initialize ChunkDescribeResponse objects (assuming ChunkDescribeResponse has default constructor and setters)
        chunk1 = new ChunkDescribeResponse();
        chunk1.setChunkId("chunk1");
        chunk1.setContent("Content of chunk 1");

        chunk2 = new ChunkDescribeResponse();
        chunk2.setChunkId("chunk2");
        chunk2.setContent("Content of chunk 2");

        chunksDescribeResponse.setData(new ChunkDescribeResponse[]{chunk1, chunk2});
        chunksDescribeResponse.setMarker("testMarker");
        chunksDescribeResponse.setTruncated(true);
        chunksDescribeResponse.setNextMarker("testNextMarker");
        chunksDescribeResponse.setMaxKeys(100);
    }

    @Test
    public void testData() {
        ChunkDescribeResponse[] data = chunksDescribeResponse.getData();
        assertNotNull(data);
        assertEquals(2, data.length);
        assertEquals("chunk1", data[0].getChunkId());
        assertEquals("Content of chunk 1", data[0].getContent());
        assertEquals("chunk2", data[1].getChunkId());
        assertEquals("Content of chunk 2", data[1].getContent());
    }

    @Test
    public void testMarker() {
        assertEquals("testMarker", chunksDescribeResponse.getMarker());
    }

    @Test
    public void testIsTruncated() {
        assertTrue(chunksDescribeResponse.isTruncated());
    }

    @Test
    public void testNextMarker() {
        assertEquals("testNextMarker", chunksDescribeResponse.getNextMarker());
    }

    @Test
    public void testMaxKeys() {
        assertEquals(Integer.valueOf(100), chunksDescribeResponse.getMaxKeys());
    }
}