package com.baidubce.appbuilder;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.dataset.Dataset;
import com.baidubce.appbuilder.model.dataset.DocumentListResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class DatasetTest {

    @Before
    public void setUp()  {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN_V3"));
    }

    // @Test
    // public void testCreateDataset() throws IOException, AppBuilderServerException {
    //     Dataset dataset = new Dataset();
        
    //     String datasetId = "";
    //     try {
    //         datasetId = dataset.createDataset("dataset_name");
    //         assertNotNull(datasetId);
    //     } catch (Exception e) {
    //         datasetId = System.getenv("DATASET_ID_V3");
    //         dataset.setDatasetId(datasetId);
    //     }
        
    //     String filePath = "src/test/java/com/baidubce/appbuilder/files/test.pdf";

    //     String[] documentIds = dataset.addDocuments(new ArrayList<>(Collections.singletonList(filePath)), false, null, false);
    //     assertNotEquals(documentIds.length, 0);

    //     DocumentListResponse resp = dataset.getDocumentList(1, 20, "");
    //     assertNotEquals(resp.getResult().getTotal(), 0);

    //     dataset.deleteDocuments(documentIds);
    // }
}
