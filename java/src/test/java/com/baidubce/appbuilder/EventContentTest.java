package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;
import java.util.HashMap;
import java.util.Map;
import static org.junit.Assert.*;

public class EventContentTest {
    private EventContent eventContent;
    private EventContent.ToolCall toolCall;

    @Before
    public void setUp() {
        eventContent = new EventContent();

        // Initialize a ToolCall object (assuming ToolCall has a constructor and setters)
        toolCall = new EventContent.ToolCall();  // Modify this if ToolCall requires parameters in the constructor

        // Set up data for the test
        eventContent.setEventCode("testEventCode");
        eventContent.setEnentMessage("testEventMessage");
        eventContent.setEventType("testEventType");
        eventContent.setEventId("testEventId");
        eventContent.setEventStatus("testEventStatus");
        eventContent.setContentType("testContentType");

        Map<String, Object> outputs = new HashMap<>();
        outputs.put("outputKey", "outputValue");
        eventContent.setOutputs(outputs);

        Map<String, Object> usage = new HashMap<>();
        usage.put("usageKey", "usageValue");
        eventContent.setUsage(usage);

        eventContent.setToolCalls(new EventContent.ToolCall[]{toolCall});
    }

    @Test
    public void testEventCode() {
        assertEquals("testEventCode", eventContent.getEventCode());
    }

    @Test
    public void testEventMessage() {
        assertEquals("testEventMessage", eventContent.getEnentMessage());
    }

    @Test
    public void testEventType() {
        assertEquals("testEventType", eventContent.getEventType());
    }

    @Test
    public void testEventId() {
        assertEquals("testEventId", eventContent.getEventId());
    }

    @Test
    public void testEventStatus() {
        assertEquals("testEventStatus", eventContent.getEventStatus());
    }

    @Test
    public void testContentType() {
        assertEquals("testContentType", eventContent.getContentType());
    }

    @Test
    public void testOutputs() {
        assertNotNull(eventContent.getOutputs());
        assertEquals("outputValue", eventContent.getOutputs().get("outputKey"));
    }

    @Test
    public void testUsage() {
        assertNotNull(eventContent.getUsage());
        assertEquals("usageValue", eventContent.getUsage().get("usageKey"));
    }

    @Test
    public void testToolCalls() {
        assertNotNull(eventContent.getToolCalls());
        assertEquals(1, eventContent.getToolCalls().length);
        assertEquals(toolCall, eventContent.getToolCalls()[0]);
    }

    @Test
    public void testToString() {
        String expectedString = "EventContent{" + "eventCode='testEventCode', eventMessage='testEventMessage', eventType='testEventType', eventId='testEventId', eventStatus='testEventStatus', contentType='testContentType', outputs={outputKey=outputValue}'" + ", usage={usageKey=usageValue}'" + ", toolCalls=" + eventContent.getToolCalls() + '}';
        assertEquals(expectedString, eventContent.toString());
    }
}