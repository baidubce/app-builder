package com.baidubce.appbuilder;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.console.appbuilderclient.AppList;

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;
import java.util.List;

import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.AppListRequest;
import com.baidubce.appbuilder.model.appbuilderclient.AppsDescribeRequest;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.model.appbuilderclient.EventContent;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class AppBuilderClientTest {
    String appId;
    String chatflowAppId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN"));
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
        appId = "aa8af334-df27-4855-b3d1-0d249c61fc08";
        chatflowAppId = "4403205e-fb83-4fac-96d8-943bdb63796f";
    }

    @Test
    public void GetAppsTest() throws IOException, AppBuilderServerException {
        AppList builder = new AppList();
        AppListRequest request = new AppListRequest();
        request.setLimit(10);
        assertNotNull(builder.getAppList(request)[0].getId());
    }

    @Test
    public void DescribeAppsTest() throws IOException, AppBuilderServerException {
        AppList appList = new AppList();
        AppsDescribeRequest request = new AppsDescribeRequest();
        assertNotNull(appList.describeApps(request).getData()[0].getId());
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
            for (Event event : result.getEvents()) {
                if (event.getContentType().equals(EventContent.JsonContentType) && (event.getEventType().equals(Event.FollowUpQueryEventType))) {
                    Object json = event.getDetail().get("json");
                    if (json instanceof Map<?,?>) {
                        Map<?, ?> map = (Map<?, ?>) json;
                        for (Map.Entry<?, ?> entry : map.entrySet()) {

                            if (entry.getKey() instanceof String && entry.getValue() instanceof List) {
                                String key = (String) entry.getKey();
                                List<?> list = (List<?>) entry.getValue();
                                if (!list.isEmpty() && list.get(0) instanceof String) {
                                    String stringValue = (String) list.get(0);
                                    if (key.equals("follow_up_querys")) {
                                        System.out.println(stringValue);
                                        assert !stringValue.isEmpty();
                                    }
                                }
                            }
                        }
                    }
                }
            }
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

        String toolJson = new String(Files.readAllBytes(Paths.get("src/test/java/com/baidubce/appbuilder/files/toolcall.json")));
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

        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "你能干什么", false);
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

    @Test
    public void AppBuilderClientRunChatflowTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(chatflowAppId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "查天气", true);
        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        Stack<String> interruptStack = new Stack<String>();
        String interruptEventId = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            for (Event event : result.getEvents()) {
                if (event.getContentType().equals(EventContent.PublishMessageContentType)) {
                    String message = event.getDetail().get("message").toString();
                    System.out.println(message);
                }
                if (event.getContentType().equals(EventContent.ChatflowInterruptContentType)) {
                    assertEquals(event.getEventType(), Event.ChatflowEventType);
                    interruptEventId = event.getDetail().get("interrupt_event_id").toString();
                    interruptStack.push(interruptEventId);
                    break;
                }
            }
        }
        assert interruptEventId != null && !interruptEventId.isEmpty();

        interruptEventId = "";
        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "我先查个航班动态",
                true);
        request2.setAction(AppBuilderClientRunRequest.Action.createAction(interruptStack.pop()));
        AppBuilderClientIterator itor2 = builder.run(request2);
        assertTrue(itor2.hasNext());
        while (itor2.hasNext()) {
            AppBuilderClientResult result2 = itor2.next();
            for (Event event : result2.getEvents()) {
                if (event.getContentType().equals(EventContent.PublishMessageContentType)) {
                    String message = event.getDetail().get("message").toString();
                    System.out.println(message);
                }
                if (event.getContentType().equals(EventContent.ChatflowInterruptContentType)) {
                    assertEquals(event.getEventType(), Event.ChatflowEventType);
                    interruptEventId = event.getDetail().get("interrupt_event_id").toString();
                    interruptStack.push(interruptEventId);
                    break;
                }
            }
        }
        assert interruptEventId != null && !interruptEventId.isEmpty();

        interruptEventId = "";
        AppBuilderClientRunRequest request3 = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "CA1234",
                true);
        request3.setAction(AppBuilderClientRunRequest.Action.createAction(interruptStack.pop()));
        AppBuilderClientIterator itor3 = builder.run(request3);
        assertTrue(itor3.hasNext());
        while (itor3.hasNext()) {
            AppBuilderClientResult result3 = itor3.next();
            for (Event event : result3.getEvents()) {
                if (event.getContentType().equals(EventContent.TextContentType)) {
                    String text = event.getDetail().get("text").toString();
                    System.out.println(text);
                }
                if (event.getContentType().equals(EventContent.ChatflowInterruptContentType)) {
                    assertEquals(event.getEventType(), Event.ChatflowEventType);
                    interruptEventId = event.getDetail().get("interrupt_event_id").toString();
                    interruptStack.push(interruptEventId);
                    break;
                }
            }
        }
        assert interruptEventId != null && !interruptEventId.isEmpty();

        boolean hasMultipleContentType = false;
        AppBuilderClientRunRequest request4 = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "北京的",
                true);
        request4.setAction(AppBuilderClientRunRequest.Action.createAction(interruptStack.pop()));
        AppBuilderClientIterator itor4 = builder.run(request4);
        assertTrue(itor4.hasNext());
        while (itor4.hasNext()) {
            AppBuilderClientResult result4 = itor4.next();
            for (Event event : result4.getEvents()) {
                if (event.getContentType().equals(EventContent.TextContentType)) {
                    String text = event.getDetail().get("text").toString();
                    System.out.println(text);
                }
                if (event.getContentType().equals(EventContent.MultipleDialogEventContentType)) {
                    assertEquals(event.getEventType(), Event.ChatflowEventType);
                    hasMultipleContentType = true;
                    break;
                }
            }
        }
        assertTrue(hasMultipleContentType);
    }
}
