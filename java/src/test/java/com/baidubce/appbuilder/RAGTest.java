package com.baidubce.appbuilder;

import org.junit.Before;
import org.junit.Test;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.rag.RAG;
import com.baidubce.appbuilder.model.rag.RAGResponse;
import java.io.IOException;
import java.util.Iterator;

import static org.junit.Assert.assertTrue;


public class RAGTest {
    String appId;
    @Before
    public void setUp()  {
        System.setProperty("APPBUILDER_TOKEN", "xxx");
        System.setProperty("GATEWAY_URL", "xxx");
        appId = "xxx";
    }
    @Test
    public void testRAG() throws IOException, AppBuilderServerException {
        RAG rag = new RAG(appId);
        Iterator<RAGResponse> itor = rag.run("合同中的甲方是谁？", "", true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            RAGResponse response = itor.next();
        }
    }
}
