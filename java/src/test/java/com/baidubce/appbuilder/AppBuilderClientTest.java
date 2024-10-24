package com.baidubce.appbuilder;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.console.appbuilderclient.AppList;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.AppListRequest;
import com.google.gson.Gson;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class AppBuilderClientTest {
    String appId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN"));
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
        appId = "aa8af334-df27-4855-b3d1-0d249c61fc08";
    }

    @Test
    public void GetAppsTest() throws IOException, AppBuilderServerException {
        AppList builder = new AppList();
        AppListRequest request = new AppListRequest();
        request.setLimit(10);
        assertNotNull(builder.getAppList(request)[0].getId());
    }

    @Test
    public void AppBuilderClientRunTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        String fileId = builder.uploadLocalFile(conversationId,
                "src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(fileId);
        AppBuilderClientIterator itor =
                builder.run("北京有多少小学生", conversationId, new String[] {fileId}, true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }

    @Test(expected = AppBuilderServerException.class)
    public void testCreateConversation_AppBuilderServerException()
            throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient("appId");
        builder.createConversation();
    }

    @Test
    public void AppBuilderClientRunFuncTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        
        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "今天北京的天气怎么样?", false);

        // 如果你本地的java版本更高，可以使用文本块特性，简化字符串构造
        String toolJson = "{\n" +
        "  \"type\": \"function\",\n" +
        "  \"function\": {\n" +
        "    \"name\": \"get_cur_whether\",\n" +
        "    \"description\": \"这是一个获得指定地点天气的工具\",\n" +
        "    \"parameters\": {\n" +
        "      \"type\": \"object\",\n" +
        "      \"properties\": {\n" +
        "        \"location\": {\n" +
        "          \"type\": \"string\",\n" +
        "          \"description\": \"省，市名，例如：河北省\"\n" +
        "        },\n" +
        "        \"unit\": {\n" +
        "          \"type\": \"string\",\n" +
        "          \"enum\": [\n" +
        "            \"摄氏度\",\n" +
        "            \"华氏度\"\n" +
        "          ]\n" +
        "        }\n" +
        "      },\n" +
        "      \"required\": [\n" +
        "        \"location\"\n" +
        "      ]\n" +
        "    }\n" +
        "  }\n" +
        "}";
        request.setTools(toolJson);

        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        String ToolCallID = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            ToolCallID = result.getEvents()[0].getToolCalls()[0].getId();
            System.out.println(result);
        }

        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest(appId, conversationId);
        request2.setToolOutputs(ToolCallID, "北京今天35度");
        AppBuilderClientIterator itor2 = builder.run(request2);
        assertTrue(itor2.hasNext());
        while (itor2.hasNext()) {
            AppBuilderClientResult result = itor2.next();
            System.out.println(result);
        }
    }
    
    @Test
    public void AppBuilderClientRunToolChoiceTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);

        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest();
        request.setAppId(appId);
        request.setConversationID(conversationId);
        request.setQuery("你能干什么");
        request.setStream(false);
        request.setEndUserId("java_test_user_0");
        Map<String, Object> input = new HashMap<>();
        input.put("city", "北京");
        AppBuilderClientRunRequest.ToolChoice.Function func = new AppBuilderClientRunRequest.ToolChoice.Function(
                "WeatherQuery", input);
        AppBuilderClientRunRequest.ToolChoice choice = new AppBuilderClientRunRequest.ToolChoice("function", func);
        request.setToolChoice(choice);

        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }
}
