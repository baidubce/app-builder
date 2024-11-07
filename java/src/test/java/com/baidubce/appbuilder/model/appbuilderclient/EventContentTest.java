package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class EventContentTest {

    private EventContent eventContent;
    private ToolCall[] toolCalls;

    @Before
    public void setUp() {
        eventContent = new EventContent();
        toolCalls = new ToolCall[]{new ToolCall(), new ToolCall()};
    }

    @Test
    public void testGetSetEventCode() {
        eventContent.setEventCode("event123");
        assertEquals("event123", eventContent.getEventCode());
    }

    @Test
    public void testGetSetEventMessage() {
        eventContent.setEnentMessage("message123");
        assertEquals("message123", eventContent.getEnentMessage());
    }

    @Test
    public void testGetSetEventType() {
        eventContent.setEventType("eventType123");
        assertEquals("eventType123", eventContent.getEventType());
    }

    @Test
    public void testGetSetEventId() {
        eventContent.setEventId("eventId123");
        assertEquals("eventId123", eventContent.getEventId());
    }

    @Test
    public void testGetSetEventStatus() {
        eventContent.setEventStatus("status123");
        assertEquals("status123", eventContent.getEventStatus());
    }

    @Test
    public void testGetSetContentType() {
        eventContent.setContentType("contentType123");
        assertEquals("contentType123", eventContent.getContentType());
    }

    @Test
    public void testGetSetOutputs() {
        Map<String, Object> outputs = new HashMap<>();
        outputs.put("key", "value");
        eventContent.setOutputs(outputs);
        assertEquals(outputs, eventContent.getOutputs());
    }

    @Test
    public void testGetSetUsage() {
        Map<String, Object> usage = new HashMap<>();
        usage.put("cpu", "80%");
        eventContent.setUsage(usage);
        assertEquals(usage, eventContent.getUsage());
    }

    @Test
    public void testGetSetToolCalls() {
        eventContent.setToolCalls(toolCalls);
        assertArrayEquals(toolCalls, eventContent.getToolCalls());
    }

    @Test
    public void testToString() {
        eventContent.setEventCode("event123");
        eventContent.setEnentMessage("message123");
        eventContent.setEventType("eventType123");
        eventContent.setEventId("eventId123");
        eventContent.setEventStatus("status123");
        eventContent.setContentType("contentType123");

        String expected = "EventContent{eventCode='event123', eventMessage='message123', eventType='eventType123', eventId='eventId123', eventStatus='status123', contentType='contentType123', outputs=null'usage=null', toolCalls=null}";
        assertEquals(expected, eventContent.toString());
    }
}