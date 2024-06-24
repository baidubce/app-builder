package com.baidubce.appbuilder;

import static org.junit.Assert.assertNotNull;

import java.io.IOException;

import org.junit.Before;
import org.junit.Test;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.knowledgebase.Knowledgebase;
import com.baidubce.appbuilder.model.knowledgebase.*;

public class KnowledgebaseTest {
    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN","");
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
    }
    
    @Test
    public void testAddDocument() throws IOException, AppBuilderServerException {
        String knowledgeBaseId  = "";
        Knowledgebase knowledgebase = new Knowledgebase();

        DocumentListRequest listRequest = new DocumentListRequest(); 
        listRequest.setKonwledgeBaseId(knowledgeBaseId);
        listRequest.setLimit(10);
        Document[] documents = knowledgebase.getDocumentList(listRequest);
        assertNotNull(documents[0].getId());


        String fileId = knowledgebase.uploadFile("src/test/java/com/baidubce/appbuilder/files/test.pdf");
        System.out.println(fileId);
        assertNotNull(fileId);

        DocumentAddRequest request = new DocumentAddRequest();
        request.setKnowledgeBaseId(knowledgeBaseId);
        request.setContentType("raw_text");
        request.setFileIds(new String[] { fileId });
        DocumentAddRequest.CustomProcessRule customProcessRule = new DocumentAddRequest.CustomProcessRule();
        customProcessRule.setSeparators(new String[] { "。" });
        customProcessRule.setTargetLength(300);
        customProcessRule.setOverlapRate(0.25);
        request.setCustomProcessRule(customProcessRule);
        String[] documentsRes = knowledgebase.addDocument(request);
        assertNotNull(documentsRes);

        DocumentDeleteRequest deleteRequest = new DocumentDeleteRequest();
        deleteRequest.setKonwledgeBaseId(knowledgeBaseId);
        deleteRequest.setDocumentId(documentsRes[0]);
        knowledgebase.deleteDocument(deleteRequest);
    }
}
