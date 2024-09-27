package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ChunkDescribeResponseTest {
    private ChunkDescribeResponse chunkDescribeResponse;

    @Before
    public void setUp() {
        chunkDescribeResponse = new ChunkDescribeResponse();
    }

    @Test
    public void testChunkId() {
        chunkDescribeResponse.setChunkId("test_chunk_id");
        assertEquals("test_chunk_id", chunkDescribeResponse.getChunkId());
    }

    @Test
    public void testType() {
        chunkDescribeResponse.setType("test_type");
        assertEquals("test_type", chunkDescribeResponse.getType());
    }

    @Test
    public void testKnowledgeBaseId() {
        chunkDescribeResponse.setKnowledgeBaseId("test_knowledge_base_id");
        assertEquals("test_knowledge_base_id", chunkDescribeResponse.getKnowledgeBaseId());
    }

    @Test
    public void testDocumentId() {
        chunkDescribeResponse.setDocumentId("test_document_id");
        assertEquals("test_document_id", chunkDescribeResponse.getDocumentId());
    }

    @Test
    public void testContent() {
        chunkDescribeResponse.setContent("test_content");
        assertEquals("test_content", chunkDescribeResponse.getContent());
    }

    @Test
    public void testWordCount() {
        chunkDescribeResponse.setWordCount(123);
        assertEquals(Integer.valueOf(123), chunkDescribeResponse.getWordCount());
    }

    @Test
    public void testTokenCount() {
        chunkDescribeResponse.setTokenCount(456);
        assertEquals(Integer.valueOf(456), chunkDescribeResponse.getTokenCount());
    }

    @Test
    public void testEnabled() {
        chunkDescribeResponse.setEnabled(true);
        assertTrue(chunkDescribeResponse.getEnabled());

        chunkDescribeResponse.setEnabled(false);
        assertFalse(chunkDescribeResponse.getEnabled());
    }

    @Test
    public void testStatus() {
        chunkDescribeResponse.setStatus("test_status");
        assertEquals("test_status", chunkDescribeResponse.getStatus());
    }

    @Test
    public void testStatusMessage() {
        chunkDescribeResponse.setStatusMessage("test_status_message");
        assertEquals("test_status_message", chunkDescribeResponse.getStatusMessage());
    }

    @Test
    public void testCreateTime() {
        chunkDescribeResponse.setCreateTime(789);
        assertEquals(Integer.valueOf(789), chunkDescribeResponse.getCreateTime());
    }

    @Test
    public void testUpdateTime() {
        chunkDescribeResponse.setUpdateTime(101112);
        assertEquals(Integer.valueOf(101112), chunkDescribeResponse.getUpdateTime());
    }
}