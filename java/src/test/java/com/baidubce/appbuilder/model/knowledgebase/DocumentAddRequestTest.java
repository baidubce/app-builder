package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;

public class DocumentAddRequestTest {

    private DocumentAddRequest documentAddRequest;
    private DocumentAddRequest.CustomProcessRule customProcessRule;

    @Before
    public void setUp() {
        documentAddRequest = new DocumentAddRequest();
        customProcessRule = new DocumentAddRequest.CustomProcessRule();
    }

    @Test
    public void testSetAndGetKnowledgeBaseId() {
        String knowledgeBaseId = "kb123";
        documentAddRequest.setKnowledgeBaseId(knowledgeBaseId);
        assertEquals(knowledgeBaseId, documentAddRequest.getKnowledgeBaseId());
    }

    @Test
    public void testSetAndGetContentType() {
        String contentType = "text";
        documentAddRequest.setContentType(contentType);
        assertEquals(contentType, documentAddRequest.getContentType());
    }

    @Test
    public void testSetAndGetIsEnhanced() {
        boolean isEnhanced = true;
        documentAddRequest.setEnhanced(isEnhanced);
        assertEquals(isEnhanced, documentAddRequest.isEnhanced());
    }

    @Test
    public void testSetAndGetFileIds() {
        String[] fileIds = {"file1", "file2"};
        documentAddRequest.setFileIds(fileIds);
        assertArrayEquals(fileIds, documentAddRequest.getFileIds());
    }

    @Test
    public void testSetAndGetCustomProcessRule() {
        String[] separators = {",", ";"};
        int targetLength = 100;
        double overlapRate = 0.5;

        customProcessRule.setSeparators(separators);
        customProcessRule.setTargetLength(targetLength);
        customProcessRule.setOverlapRate(overlapRate);

        documentAddRequest.setCustomProcessRule(customProcessRule);

        assertArrayEquals(separators, documentAddRequest.getCustomProcessRule().getSeparators());
        assertEquals(targetLength, documentAddRequest.getCustomProcessRule().getTargetLength());
        assertEquals(overlapRate, documentAddRequest.getCustomProcessRule().getOverlapRate(), 0);
    }
}