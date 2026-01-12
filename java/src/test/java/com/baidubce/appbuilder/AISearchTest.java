package com.baidubce.appbuilder;

import static org.junit.Assert.assertTrue;

import java.io.IOException;

import org.junit.Before;
import org.junit.Test;
import com.google.gson.Gson;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.aisearch.AISearch;
import com.baidubce.appbuilder.model.aisearch.AISearchIterator;
import com.baidubce.appbuilder.model.aisearch.AISearchRequest;
import com.baidubce.appbuilder.model.aisearch.AISearchResponse;

public class AISearchTest {
    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN"));
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
    }

    @Test
    public void TestBaseSearch() throws IOException, AppBuilderServerException {
        AISearch client = new AISearch();
        AISearchRequest request = new AISearchRequest();
        AISearchRequest.Message[] messages = { new AISearchRequest.Message("user", "查询今天天气") };
        request.setMessages(messages);
        AISearchIterator iter = client.run(request);
        while (iter.hasNext()) {
            AISearchResponse response = iter.next();
            Gson gson = new Gson();
            String json = gson.toJson(response);
            System.out.println(json);
            assertTrue(response.getReferences().size() > 0);
        }
    }

    @Test
    public void TestAISearch() throws IOException, AppBuilderServerException {
        AISearch client = new AISearch();
        AISearchRequest request = new AISearchRequest();
        AISearchRequest.Message[] messages = { new AISearchRequest.Message("user", "查询今天天气") };
        request.setMessages(messages).setModel("deepseek-v3.1-250821");
        AISearchIterator iter = client.run(request);
        while (iter.hasNext()) {
            AISearchResponse response = iter.next();
            Gson gson = new Gson();
            String json = gson.toJson(response);
            System.out.println(json);
            assertTrue(response.getReferences().size() > 0);
        }
    }

    @Test
    public void TestAISearchStream() throws IOException, AppBuilderServerException {
        AISearch client = new AISearch();
        AISearchRequest request = new AISearchRequest();
        AISearchRequest.Message[] messages = { new AISearchRequest.Message("user", "查询今天天气") };
        request.setMessages(messages).setModel("deepseek-v3.1-250821").setStream(true);
        AISearchIterator iter = client.run(request);
        while (iter.hasNext()) {
            AISearchResponse response = iter.next();
            Gson gson = new Gson();
            String json = gson.toJson(response);
            System.out.println(json);
        }
    }
}
