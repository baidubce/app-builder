package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Arrays;

public class DocumentAddResultTest {
    private DocumentAddResult documentAddResult;

    @Before
    public void setUp() {
        documentAddResult = new DocumentAddResult();
        documentAddResult.setDatasetId("testDatasetId");
        documentAddResult.setDocumentIds(new String[] { "doc1", "doc2", "doc3" });
    }

    @Test
    public void testGetDatasetId() {
        assertEquals("testDatasetId", documentAddResult.getDatasetId());
    }

    @Test
    public void testSetDatasetId() {
        documentAddResult.setDatasetId("newDatasetId");
        assertEquals("newDatasetId", documentAddResult.getDatasetId());
    }

    @Test
    public void testGetDocumentIds() {
        String[] documentIds = documentAddResult.getDocumentIds();
        assertNotNull(documentIds);
        assertArrayEquals(new String[] { "doc1", "doc2", "doc3" }, documentIds);
    }

    @Test
    public void testSetDocumentIds() {
        documentAddResult.setDocumentIds(new String[] { "docA", "docB" });
        assertArrayEquals(new String[] { "docA", "docB" }, documentAddResult.getDocumentIds());
    }

    @Test
    public void testToString() {
        String expectedString = "DocumentAddResult{" +
                "datasetId='testDatasetId'" +
                ", documentIds=" + Arrays.toString(new String[] { "doc1", "doc2", "doc3" }) +
                '}';
        assertEquals(expectedString, documentAddResult.toString());
    }
}