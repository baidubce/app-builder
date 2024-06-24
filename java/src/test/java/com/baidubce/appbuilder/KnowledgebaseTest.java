package com.baidubce.appbuilder;

import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNotNull;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

import org.junit.Before;
import org.junit.Test;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.knowledgebase.Knowledgebase;


public class KnowledgebaseTest {
    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN",
                "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd");
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
    }
    
    @Test
    public void testUploadFile() throws IOException, AppBuilderServerException {
        Knowledgebase knowledgebase = new Knowledgebase();
        String url = knowledgebase.uploadFile("src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(url);
    }
}
