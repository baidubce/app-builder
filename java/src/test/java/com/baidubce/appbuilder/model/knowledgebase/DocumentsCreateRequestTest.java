package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DocumentsCreateRequestTest {
    private DocumentsCreateRequest documentsCreateRequest;
    private DocumentsCreateRequest.Source source;
    private DocumentsCreateRequest.ProcessOption processOption;
    private DocumentsCreateRequest.ProcessOption.Parser parser;
    private DocumentsCreateRequest.ProcessOption.Chunker chunker;
    private DocumentsCreateRequest.ProcessOption.Chunker.Separator separator;
    private DocumentsCreateRequest.ProcessOption.Chunker.Pattern pattern;
    private DocumentsCreateRequest.ProcessOption.KnowledgeAugmentation knowledgeAugmentation;

    @Before
    public void setUp() {
        // Initialize inner classes
        parser = new DocumentsCreateRequest.ProcessOption.Parser(new String[]{"choice1", "choice2"});
        separator = new DocumentsCreateRequest.ProcessOption.Chunker.Separator(
                new String[]{","}, 100, 0.5);
        pattern = new DocumentsCreateRequest.ProcessOption.Chunker.Pattern(
                "start", "\\w+", 200, 0.3);
        chunker = new DocumentsCreateRequest.ProcessOption.Chunker(
                new String[]{"chunkChoice1"}, separator, pattern, new String[]{"info1"});
        knowledgeAugmentation = new DocumentsCreateRequest.ProcessOption.KnowledgeAugmentation(
                new String[]{"augment1", "augment2"});

        processOption = new DocumentsCreateRequest.ProcessOption(
                "template1", parser, chunker, knowledgeAugmentation);
        source = new DocumentsCreateRequest.Source("url", new String[]{"http://example.com"}, 2);

        // Initialize main class
        documentsCreateRequest = new DocumentsCreateRequest(
                "knowledge_base_1", "text/plain", source, processOption);
    }

    @Test
    public void testKnowledgeBaseId() {
        assertEquals("knowledge_base_1", documentsCreateRequest.getKnowledgeBaseId());
    }

    @Test
    public void testContentFormat() {
        assertEquals("text/plain", documentsCreateRequest.getContentFormat());
    }

    @Test
    public void testSource() {
        assertEquals("url", documentsCreateRequest.getSource().getType());
        assertArrayEquals(new String[]{"http://example.com"}, documentsCreateRequest.getSource().getUrls());
        assertEquals(Integer.valueOf(2), documentsCreateRequest.getSource().getUrlDepth());
    }

    @Test
    public void testProcessOption() {
        assertEquals("template1", documentsCreateRequest.getProcessOption().getTemplate());

        // Test Parser
        assertArrayEquals(new String[]{"choice1", "choice2"}, documentsCreateRequest.getProcessOption().getParser().getChoices());

        // Test Chunker
        assertArrayEquals(new String[]{"chunkChoice1"}, documentsCreateRequest.getProcessOption().getChunker().getChoices());
        assertArrayEquals(new String[]{"info1"}, documentsCreateRequest.getProcessOption().getChunker().getPrependInfo());

        // Test Separator
        assertArrayEquals(new String[]{","}, documentsCreateRequest.getProcessOption().getChunker().getSeparator().getSeparators());
        assertEquals(Integer.valueOf(100), documentsCreateRequest.getProcessOption().getChunker().getSeparator().getTargetLength());
        assertEquals(Double.valueOf(0.5), documentsCreateRequest.getProcessOption().getChunker().getSeparator().getOverlapRate());

        // Test Pattern
        assertEquals("start", documentsCreateRequest.getProcessOption().getChunker().getPattern().getMarkPosition());
        assertEquals("\\w+", documentsCreateRequest.getProcessOption().getChunker().getPattern().getRegex());
        assertEquals(Integer.valueOf(200), documentsCreateRequest.getProcessOption().getChunker().getPattern().getTargetLength());
        assertEquals(Double.valueOf(0.3), documentsCreateRequest.getProcessOption().getChunker().getPattern().getOverlapRate());

        // Test Knowledge Augmentation
        assertArrayEquals(new String[]{"augment1", "augment2"}, documentsCreateRequest.getProcessOption().getKnowledgeAugmentation().getChoices());
    }
}