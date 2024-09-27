package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DocumentTest {
    private Document document;
    private Document.Meta meta;

    @Before
    public void setUp() {
        document = new Document();
        meta = new Document.Meta();
    }

    @Test
    public void testId() {
        document.setId("doc123");
        assertEquals("doc123", document.getId());
    }

    @Test
    public void testName() {
        document.setName("Test Document");
        assertEquals("Test Document", document.getName());
    }

    @Test
    public void testCreatedAt() {
        document.setCreatedAt("2024-01-01T00:00:00Z");
        assertEquals("2024-01-01T00:00:00Z", document.getCreatedAt());
    }

    @Test
    public void testWordCount() {
        document.setWordCount(500);
        assertEquals(500, document.getWordCount());
    }

    @Test
    public void testEnabled() {
        document.setEnabled(true);
        assertTrue(document.isEnabled());

        document.setEnabled(false);
        assertFalse(document.isEnabled());
    }

    @Test
    public void testMeta() {
        meta.setSource("http://example.com");
        meta.setFileId("file123");

        document.setMeta(meta);

        assertEquals("http://example.com", document.getMeta().getSource());
        assertEquals("file123", document.getMeta().getFileId());
    }
}