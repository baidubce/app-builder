package com.baidubce.appbuilder;


import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertTrue;

import java.io.IOException;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.rag.RAG;
import com.baidubce.appbuilder.model.rag.RAGResponse;
import com.baidubce.appbuilder.model.rag.RAGIterator;


public class RAGTest {
    String appId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", "xxx");
        System.setProperty("GATEWAY_URL", "xxx");
        appId = "xxx";
    }

    @Test
    public void testRAG() throws IOException, AppBuilderServerException {
        RAG rag = new RAG(appId);
        RAGIterator itor = rag.run("合同中的甲方是谁？", "", true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            RAGResponse response = itor.next();
        }
    }
}
