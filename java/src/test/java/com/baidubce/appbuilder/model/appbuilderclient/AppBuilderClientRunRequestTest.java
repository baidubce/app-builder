package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;

public class AppBuilderClientRunRequestTest {
    private AppBuilderClientRunRequest request;
    private AppBuilderClientRunRequest.Tool tool;
    private AppBuilderClientRunRequest.Tool.Function toolFunction;
    private AppBuilderClientRunRequest.ToolOutput toolOutput;
    private AppBuilderClientRunRequest.ToolChoice toolChoice;
    private AppBuilderClientRunRequest.ToolChoice.Function toolChoiceFunction;

    @Before
    public void setUp() {
        // Initialize Tool and Tool.Function
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("param1", "value1");
        toolFunction = new AppBuilderClientRunRequest.Tool.Function("testFunction", "testDescription", parameters);
        tool = new AppBuilderClientRunRequest.Tool("testType", toolFunction);

        // Initialize ToolOutput
        toolOutput = new AppBuilderClientRunRequest.ToolOutput("toolCallID1", "output1");

        // Initialize ToolChoice and ToolChoice.Function
        Map<String, Object> input = new HashMap<>();
        input.put("input1", "value1");
        toolChoiceFunction = new AppBuilderClientRunRequest.ToolChoice.Function("choiceFunction", input);
        toolChoice = new AppBuilderClientRunRequest.ToolChoice("choiceType", toolChoiceFunction);

        // Initialize main class
        request = new AppBuilderClientRunRequest();
        request.setAppId("testAppId");
        request.setQuery("testQuery");
        request.setStream(true);
        request.setConversationID("testConversationId");
        request.setEndUserId("testEndUserId");
        request.setTools(new AppBuilderClientRunRequest.Tool[]{tool});
        request.setToolOutputs(new AppBuilderClientRunRequest.ToolOutput[]{toolOutput});
        request.setToolChoice(toolChoice);
    }

    @Test
    public void testAppId() {
        assertEquals("testAppId", request.getAppId());
    }

    @Test
    public void testQuery() {
        assertEquals("testQuery", request.getQuery());
    }

    @Test
    public void testStream() {
        assertTrue(request.isStream());
    }

    @Test
    public void testConversationID() {
        assertEquals("testConversationId", request.getConversationID());
    }

    @Test
    public void testEndUserId() {
        assertEquals("testEndUserId", request.getEndUserId());
    }

    @Test
    public void testTools() {
        assertEquals(1, request.getTools().length);
        assertEquals("testType", request.getTools()[0].getType());
        assertEquals("testFunction", request.getTools()[0].getFunction().getName());
        assertEquals("testDescription", request.getTools()[0].getFunction().getDescription());
        assertEquals("value1", request.getTools()[0].getFunction().getParameters().get("param1"));
    }

    @Test
    public void testToolOutputs() {
        assertEquals(1, request.getToolOutputs().length);
        assertEquals("toolCallID1", request.getToolOutputs()[0].getToolCallID());
        assertEquals("output1", request.getToolOutputs()[0].getOutput());
    }

    @Test
    public void testToolChoice() {
        assertEquals("choiceType", request.getToolChoice().getType());
        assertEquals("choiceFunction", request.getToolChoice().getFunction().getName());
        assertEquals("value1", request.getToolChoice().getFunction().getInput().get("input1"));
    }

    @Test
    public void testToolFunction() {
        assertEquals("testFunction", toolFunction.getName());
        assertEquals("testDescription", toolFunction.getDescription());
        assertEquals("value1", toolFunction.getParameters().get("param1"));
    }

    @Test
    public void testToolChoiceFunction() {
        assertEquals("choiceFunction", toolChoiceFunction.getName());
        assertEquals("value1", toolChoiceFunction.getInput().get("input1"));
    }
}