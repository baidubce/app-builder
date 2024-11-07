package com.baidubce.appbuilder.model.agentbuilder;

import org.junit.Before;
import org.junit.Test;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class EventContentTest {
    private EventContent eventContent;

    @Before
    public void setUp() {
        eventContent = new EventContent();

        Map<String, Object> outputs = new HashMap<>();
        outputs.put("key1", "value1");
        outputs.put("key2", 100);

        eventContent.setEventCode("event123");
        eventContent.setEnentMessage("Event message");
        eventContent.setEventType("EventType");
        eventContent.setEventId("eventId123");
        eventContent.setEventStatus("success");
        eventContent.setContentType("application/json");
        eventContent.setOutputs(outputs);
    }

    @Test
    public void testEventCode() {
        assertEquals("event123", eventContent.getEventCode());
    }

    @Test
    public void testEnentMessage() {
        assertEquals("Event message", eventContent.getEnentMessage());
    }

    @Test
    public void testEventType() {
        assertEquals("EventType", eventContent.getEventType());
    }

    @Test
    public void testEventId() {
        assertEquals("eventId123", eventContent.getEventId());
    }

    @Test
    public void testEventStatus() {
        assertEquals("success", eventContent.getEventStatus());
    }

    @Test
    public void testContentType() {
        assertEquals("application/json", eventContent.getContentType());
    }

    @Test
    public void testOutputs() {
        Map<String, Object> outputs = eventContent.getOutputs();
        assertNotNull(outputs);
        assertEquals(2, outputs.size());
        assertEquals("value1", outputs.get("key1"));
        assertEquals(100, outputs.get("key2"));
    }

    @Test
    public void testToString() {
        String expectedString = "EventContent{" +
                "eventCode='event123'" +
                ", enentMessage='Event message'" +
                ", eventType='EventType'" +
                ", eventId='eventId123'" +
                ", eventStatus='success'" +
                ", contentType='application/json'" +
                ", outputs={key1=value1, key2=100}" +
                '}';
        assertEquals(expectedString, eventContent.toString());
    }
}